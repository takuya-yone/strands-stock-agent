from strands import Agent
from strands_tools import file_write

from strands_stock_agent.agent_tools import (
    get_market_status,
    get_market_summary,
    get_stock_info,
)

NOVA_2_LITE_GLOBAL = "global.amazon.nova-2-lite-v1:0"

NOVA_PRO_APAC = "apac.amazon.nova-pro-v1:0"

search_agent_tools = [get_stock_info, get_market_status, get_market_summary]

search_system_prompt = """
You are an expert stock market information agent. 
Provide stock information in response to user requests.
Perform a web search if necessary.
Always provide the most up-to-date information.
Answer in the language used by the user.

After responding, please use file_write to create a concise report in Markdown format.
"""

search_agent = Agent(name="strands-stock-search-agent", model=NOVA_PRO_APAC,system_prompt=search_system_prompt, tools=search_agent_tools,callback_handler=None)




report_system_prompt = """
You are an expert stock market report agent.
Create concise reports in Markdown format based on the information provided.
Don't modify the provided information.
Create a Markdown file under the '''reports''' directory.
Answer in the language used by the user.
"""

report_agent_tools = [file_write]

report_agent = Agent(name="strands-stock-report-agent", model=NOVA_2_LITE_GLOBAL,system_prompt=report_system_prompt, tools=report_agent_tools,callback_handler=None)