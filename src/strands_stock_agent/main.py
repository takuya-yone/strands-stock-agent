from strands_stock_agent.agents import report_agent, search_agent

if __name__ == "__main__":
    result = search_agent("NVIDIAの株式情報を教えて。")
    report_agent(str(result))
