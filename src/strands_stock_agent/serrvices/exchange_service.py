import yfinance as yf
from nanoid import generate

from strands_stock_agent.db.balance_db import UserBalanceModel
from strands_stock_agent.logger import logger
from strands_stock_agent.schemas import (
    CurrencyEnum,
    ExchangeIndexEnum,
    OrderRequest,
    OrderResponse,
)
from strands_stock_agent.serrvices.common import get_timestamp


def exec_order(req: OrderRequest) -> OrderResponse:
    """
    Execute a currency exchange order.

    Args:
        req (OrderRequest): The order request containing user ID, sell currency, buy currency, and quantity.

    Returns:
        OrderResponse: The response containing the transaction ID and timestamp.
    """
    logger.info(f"Executing order for user: {req.user_id}, sell: {req.sell}, buy: {req.buy}, quantity: {req.quantity}")
    transaction_id = generate()
    timestamp = get_timestamp()

    new_balance = UserBalanceModel.get(req.user_id)



    if req.sell == CurrencyEnum.JPY:
        new_balance.JPY -= req.quantity
    elif req.sell == CurrencyEnum.USD:
        new_balance.USD -= req.quantity
    elif req.sell == CurrencyEnum.EUR:
        new_balance.EUR -= req.quantity
    elif req.sell == CurrencyEnum.GBP:
        new_balance.GBP -= req.quantity

    if req.buy == CurrencyEnum.JPY:
        new_balance.JPY += req.quantity
    elif req.buy == CurrencyEnum.USD:
        new_balance.USD += req.quantity
    elif req.buy == CurrencyEnum.EUR:
        new_balance.EUR += req.quantity
    elif req.buy == CurrencyEnum.GBP:
        new_balance.GBP += req.quantity

    save_balance(req.user_id, new_balance)

    res = OrderResponse(transaction_id=transaction_id, timestamp=timestamp)
    return res


def save_balance(user_id: str, new_balance: UserBalanceModel):
    """
    Save the updated user balance to the database.

    Args:
        user_id (str): The user ID for which to save the balance.
        new_balance (UserBalanceModel): The updated balance object.
    """
    balance = UserBalanceModel.get(user_id)
    balance.JPY = new_balance.JPY
    balance.USD = new_balance.USD
    balance.EUR = new_balance.EUR
    balance.GBP = new_balance.GBP
    balance.TOTAL_JPY_VALUE = calc_jpy_value(new_balance)
    balance.save()



def calc_jpy_value(balance:UserBalanceModel):
    """
    Calculate the total value of the user's balance in JPY.

    Args:
        balance (UserBalanceModel): The user's balance object.

    Returns:
        int: The total value of the balance in JPY.
    """
    jpy_value = balance.JPY

    jpy_value += balance.USD * get_last_price(ExchangeIndexEnum.USDJPY)
    jpy_value += balance.EUR * get_last_price(ExchangeIndexEnum.EURJPY)
    jpy_value += balance.GBP * get_last_price(ExchangeIndexEnum.GBPJPY)

    return int(jpy_value)



def get_last_price(ticker:ExchangeIndexEnum) -> float:
    """
    Get the last price for the given exchange ticker.

    Args:
        ticker (ExchangeIndexEnum): The exchange ticker symbol.

    Returns:
        float: The last price of the exchange ticker.
    """
    exchange = yf.Ticker(ticker.value).fast_info["lastPrice"]
    return exchange