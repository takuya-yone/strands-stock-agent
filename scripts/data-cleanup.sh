#!/usr/bin/env bash
#
# DynamoDB 2テーブルの全レコード削除 + S3バケットを空にする
# 依存: aws cli v2, jq
#
# 使い方:
#   ./cleanup.sh            # 確認プロンプトあり
#   ./cleanup.sh --yes      # 確認なしで実行
#
set -euo pipefail

# ===== 設定（環境に合わせて変更） =====
TABLE1="FxBalanceHistoryTable"
TABLE2="FxOrderHistoryTable"
BUCKET="fx-order-summary-bucket"
export AWS_REGION="${AWS_REGION:-ap-northeast-1}"
export AWS_DEFAULT_REGION="$AWS_REGION"
# export AWS_PROFILE="my-profile"
# ======================================

command -v aws >/dev/null || { echo "aws cli が必要です" >&2; exit 1; }
command -v jq  >/dev/null || { echo "jq が必要です" >&2; exit 1; }

echo "リージョン : $AWS_REGION"
echo "対象テーブル: $TABLE1, $TABLE2 (全レコード削除)"
echo "対象バケット: s3://$BUCKET (全オブジェクト削除)"
echo "アカウント  : $(aws sts get-caller-identity --query Account --output text)"

if [[ "${1:-}" != "--yes" ]]; then
  read -r -p "本当に実行しますか？ 'yes' と入力してください: " ans
  [[ "$ans" == "yes" ]] || { echo "中止しました"; exit 1; }
fi

# ---------- DynamoDB: 全件削除 ----------
empty_table() {
  local table="$1"
  echo "=== DynamoDB: $table ==="

  # キー属性名を取得し、予約語対策で ExpressionAttributeNames を組み立てる
  local keys names proj
  keys=$(aws dynamodb describe-table --table-name "$table" \
           --query 'Table.KeySchema[].AttributeName' --output json)
  names=$(jq -c 'to_entries | map({key: ("#k\(.key)"), value: .value}) | from_entries' <<<"$keys")
  proj=$(jq -r 'to_entries | map("#k\(.key)") | join(",")' <<<"$keys")

  local total=0 start_key=""
  while :; do
    local args=(dynamodb scan --table-name "$table"
                --projection-expression "$proj"
                --expression-attribute-names "$names"
                --output json --no-paginate)
    [[ -n "$start_key" ]] && args+=(--exclusive-start-key "$start_key")

    local page
    page=$(aws "${args[@]}")

    # 25件ずつに分割して BatchWriteItem
    while IFS= read -r chunk; do
      [[ -z "$chunk" ]] && continue
      local req
      req=$(jq -c --arg t "$table" '{($t): map({DeleteRequest: {Key: .}})}' <<<"$chunk")

      # UnprocessedItems があれば再試行
      local tries=0
      while :; do
        local res unprocessed
        res=$(aws dynamodb batch-write-item --request-items "$req" --output json)
        unprocessed=$(jq -c '.UnprocessedItems' <<<"$res")
        [[ "$unprocessed" == "{}" ]] && break
        req="$unprocessed"
        tries=$((tries + 1))
        [[ $tries -gt 10 ]] && { echo "リトライ上限に達しました" >&2; exit 1; }
        sleep $((tries < 5 ? tries : 5))
      done
      total=$((total + $(jq 'length' <<<"$chunk")))
    done < <(jq -c '.Items as $a | range(0; ($a|length); 25) as $i | $a[$i:$i+25]' <<<"$page")

    echo "  削除済み: $total 件"

    start_key=$(jq -c '.LastEvaluatedKey // empty' <<<"$page")
    [[ -z "$start_key" ]] && break
  done
  echo "  完了: $table ($total 件)"
}

# ---------- S3: バケットを空にする ----------
empty_bucket() {
  local bucket="$1"
  echo "=== S3: s3://$bucket ==="

  # 現行オブジェクトを削除
  aws s3 rm "s3://$bucket" --recursive --only-show-errors

  # バージョニング有効の場合: 全バージョン・削除マーカーも削除
  while :; do
    local out payload count
    out=$(aws s3api list-object-versions --bucket "$bucket" --max-items 1000 --output json)
    payload=$(jq -c '{Objects: ([(.Versions // [])[], (.DeleteMarkers // [])[]]
                       | map({Key: .Key, VersionId: .VersionId})), Quiet: true}' <<<"$out")
    count=$(jq '.Objects | length' <<<"$payload")
    [[ "$count" -eq 0 ]] && break
    aws s3api delete-objects --bucket "$bucket" --delete "$payload" >/dev/null
    echo "  バージョン削除: $count 件"
  done
  echo "  完了: s3://$bucket"
}

empty_table "$TABLE1"
empty_table "$TABLE2"
empty_bucket "$BUCKET"

echo "すべて完了しました"