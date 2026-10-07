import os

from strands_stock_agent.agents import report_agent, search_agent

if __name__ == "__main__":
    os.environ["BYPASS_TOOL_CONSENT"] = "true"
    
    result = search_agent("Appleの株式情報/財務情報を教えて。")
    report_agent(str(result))
