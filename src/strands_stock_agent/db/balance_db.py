from pynamodb.attributes import MapAttribute, NumberAttribute, UnicodeAttribute
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from pynamodb.models import Model

from strands_stock_agent.schemas import FxBalance


class UserBalanceModel(Model):
    """
    A DynamoDB User Balance
    """

    class Meta:
        table_name = "fx-balance-table"

    userId = UnicodeAttribute(hash_key=True)
    balance = MapAttribute(JPY=NumberAttribute(), USD=NumberAttribute(), EUR=NumberAttribute(), GBP=NumberAttribute())
    latestTransactionId = UnicodeAttribute(null=True)

    def to_fx_balance(self) -> FxBalance:
        return FxBalance(JPY=self.balance.JPY, USD=self.balance.USD, EUR=self.balance.EUR, GBP=self.balance.GBP)


class UserBalanceHistoryModel(Model):
    """
    A DynamoDB User Balance History
    """

    class Meta:
        table_name = "fx-balance-history-table"

    userId = UnicodeAttribute(hash_key=True)
    timestamp = UnicodeAttribute(range_key=True)
    transactionId = UnicodeAttribute()
    balance = MapAttribute(JPY=NumberAttribute(), USD=NumberAttribute(), EUR=NumberAttribute(), GBP=NumberAttribute())
    totalJpyValue = NumberAttribute()


class UserIdIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = "user-id-index"
        projection = AllProjection()
        # プロビジョニングモードの場合のみ必要
        # read_capacity_units = 1
        # write_capacity_units = 1

    # GSIのパーティションキー
    userId = UnicodeAttribute(hash_key=True)
    # GSIのソートキー(任意)
    timestamp = UnicodeAttribute(range_key=True)


class OrderHistoryModel(Model):
    """
    A DynamoDB Order History
    """

    class Meta:
        table_name = "fx-order-history-table"

    transactionId = UnicodeAttribute(hash_key=True)
    userId = UnicodeAttribute()
    timestamp = UnicodeAttribute()
    ticker = UnicodeAttribute()
    quantity = NumberAttribute()
    price = NumberAttribute()
    order_summary = UnicodeAttribute(null=True)

    # インデックスをクラス属性として登録
    user_id_index = UserIdIndex()
