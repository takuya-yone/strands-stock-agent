import os

from strands_stock_agent.agents import exchange_report_agent
from strands_stock_agent.agents.exchange_exec_agent import exchange_exec_agent

if __name__ == "__main__":
    os.environ["BYPASS_TOOL_CONSENT"] = "true"

    # result = search_agent("米ドルの情報")
    # report_agent(str(result))

    # exchange_result = exchange_exec_agent("為替残高を調べて。大きく動いた通貨の買い注文を入れたい")
    exchange_result = exchange_exec_agent(
        "良さそうな通貨があれば注文を入れて。利益最大化を目指して積極的に取引して。過去の取引履歴も参考にすること"
    )
    # exchange_result = exchange_exec_agent("インテルの最新株価")
    # exchange_result = exchange_exec_agent("ツールの一覧")
    exchange_report_agent(str(exchange_result))
