import os

from strands_stock_agent.agents import exchange_exec_agent, exchange_report_agent

if __name__ == "__main__":
    os.environ["BYPASS_TOOL_CONSENT"] = "true"

    # result = search_agent("米ドルの情報")
    # report_agent(str(result))

    # exchange_result = exchange_exec_agent("為替残高を調べて。大きく動いた通貨の買い注文を入れたい")
    exchange_result = exchange_exec_agent("良さそうな通貨があれば注文を入れて。利益最大化を目指して積極的に取引して")
    print("--------")
    print(exchange_result)
    print("--------")
    exchange_report_agent(str(exchange_result))
