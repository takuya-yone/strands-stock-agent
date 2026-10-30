from strands import Agent

from strands_stock_agent.schemas import StrandsLlmModelEnum
from strands_stock_agent.tools import (
    get_exchange_info,
    get_fx_balance,
    order,
)

exchange_exec_agent_tools = [get_exchange_info, get_fx_balance, order]


exchange_system_prompt = """
You are an expert foreign exchange information agent. 
Provide exchange rate information in response to user requests.
Perform a web search if necessary.
Always provide the most up-to-date information.
Base your thinking on Japanese yen.
You can retrieve your foreign exchange account balance.
Answer in Japanese.
UserId is 'test_user'.
"""

exchange_exec_agent = Agent(
    name="strands-exchange-exec-agent",
    model=StrandsLlmModelEnum.KIMI_K3_GLOBAL.value,
    system_prompt=exchange_system_prompt,
    tools=exchange_exec_agent_tools,
    callback_handler=None,
)
