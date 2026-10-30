from strands import Agent
from strands_tools import file_write

from strands_stock_agent.schemas import StrandsLlmModelEnum

report_system_prompt = """
You are an expert currency exchange report agent.
Based on the provided information, briefly summarize the thought process behind foreign exchange trading.Create a Markdown file under the '''reports''' directory.
Create report in Japanese.
"""

exchange_report_agent_tools = [file_write]

report_agent = Agent(
    name="strands-exchange-report-agent",
    model=StrandsLlmModelEnum.NOVA_2_LITE_GLOBAL.value,
    system_prompt=report_system_prompt,
    tools=exchange_report_agent_tools,
    callback_handler=None,
)
