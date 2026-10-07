from strands import Agent
from strands_tools import file_write

from strands_stock_agent.agent_tools import (
    get_market_status,
    get_market_summary,
    get_stock_financial_statement,
    get_stock_info,
)
from strands_stock_agent.schemas import StrandsLlmModelEnum

search_agent_tools = [get_stock_info, get_market_status, get_market_summary,get_stock_financial_statement]


search_system_prompt = """
You are an expert stock market information agent. 
Provide stock information in response to user requests.
Perform a web search if necessary.
Always provide the most up-to-date information.
Answer in Japanese.

After responding, please use file_write to create a concise report in Markdown format.
"""

search_agent = Agent(name="strands-stock-search-agent", model=StrandsLlmModelEnum.KIMI_K3_GLOBAL.value, system_prompt=search_system_prompt, tools=search_agent_tools,callback_handler=None)




report_system_prompt = """
You are an expert stock market report agent.
Create concise reports in Markdown format based on the information provided.
Don't modify the provided information.
Create a Markdown file under the '''reports''' directory.
Create report in Japanese.
"""

report_agent_tools = [file_write]

report_agent = Agent(name="strands-stock-report-agent", model=StrandsLlmModelEnum.NOVA_2_LITE_GLOBAL.value, system_prompt=report_system_prompt, tools=report_agent_tools,callback_handler=None)