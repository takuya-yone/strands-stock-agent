from strands import Agent
from strands_tools import file_write

from strands_stock_agent.agent_tools import (
    get_market_status,
    get_market_summary,
    get_stock_info,
)

# Bedrock is the default, so no model object is needed.

NOVA_2_LITE_GLOBAL = "global.amazon.nova-2-lite-v1:0"

NOVA_PRO_APAC = "apac.amazon.nova-pro-v1:0"

agent_tools = [get_stock_info, get_market_status, get_market_summary,file_write]

system_prompt = """
You are an expert stock market information agent. 
Provide stock information in response to user requests.
Perform a web search if necessary.
Always provide the most up-to-date information.
Answer in the language used by the user.

After responding, please use file_write to create a concise report in Markdown format.
"""

agent = Agent(name="strands-stock-agent", model=NOVA_2_LITE_GLOBAL, tools=agent_tools)
# agent("最近の株式情報を教えて")




if __name__ == "__main__":
    agent("NVIDIAの株式情報を教えて")
    # agent("アジアのマーケット情報")
    # agent.tool.file_write(
    #     path="report.md",
    #     content="Hello World!"
    # )