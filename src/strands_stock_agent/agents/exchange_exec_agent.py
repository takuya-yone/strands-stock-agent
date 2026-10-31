from strands import Agent

from strands_stock_agent.schemas import StrandsLlmModelEnum
from strands_stock_agent.tools import (
    generate_transaction_id,
    get_exchange_info,
    get_fx_balance,
    get_order_histories,
    order,
)

exchange_exec_agent_tools = [get_exchange_info, get_fx_balance, order, generate_transaction_id, get_order_histories]


exchange_system_prompt = """
You are an expert foreign exchange information agent. 
Provide exchange rate information in response to user requests.
Always provide the most up-to-date information.
Base your thinking on Japanese yen.
You can retrieve your foreign exchange account balance.
Always issue a transaction ID when placing an order.
Answer in Japanese.
ActorId is 'test_user'.
Execute the order only once.
Refer to your past orders. 
Always include JPY in transactions.
"""

exchange_exec_agent = Agent(
    name="strands-exchange-exec-agent",
    model=StrandsLlmModelEnum.KIMI_K3_GLOBAL.value,
    system_prompt=exchange_system_prompt,
    tools=exchange_exec_agent_tools,
    # callback_handler=None,
)
