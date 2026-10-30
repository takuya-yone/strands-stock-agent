import os

from strands_stock_agent.agents import report_agent, search_agent, exchange_agent

if __name__ == "__main__":
    os.environ["BYPASS_TOOL_CONSENT"] = "true"
    
    # result = search_agent("米ドルの情報")
    # report_agent(str(result))

    # exchange_result = exchange_agent("為替残高を調べて。大きく動いた通貨の買い注文を入れたい")
    exchange_result = exchange_agent("為替残高を調べて。良さそうな通貨があれば買い注文を入れて")
    # report_agent(str(exchange_result))
