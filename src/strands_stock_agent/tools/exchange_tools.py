import yfinance as yf
from strands import tool

from strands_stock_agent.db.balance_db import UserBalanceModel
from strands_stock_agent.logger import logger
from strands_stock_agent.schemas import (
    CurrencyEnum,
    ExchangeIndexEnum,
    FxBalance,
    OrderRequest,
    OrderResponse,
)
from strands_stock_agent.serrvices.exchange_service import exec_order


@tool
def get_exchange_info(ticker:ExchangeIndexEnum) -> dict:
    """
    Get exchange information for the given ticker symbol.

    Ref. https://ranaroussi.github.io/yfinance/reference/api/yfinance.Ticker.html#yfinance.Ticker

    Args:
        ticker (ExchangeIndexEnum): The exchange ticker symbol.

    Returns:
        dict: A dictionary containing stock information.
    """
    logger.info(f"Fetching exchange information for ticker: {ticker}", extra={"ticker": ticker})
    exchange = yf.Ticker(ticker.value)
    return exchange.info


@tool
def get_fx_balance(user_id:str) -> FxBalance:
    """
    Get the current foreign exchange balance.

    Args:
        user_id (str): The user ID for which to fetch the FX balance.

    Returns:
        FxBalance: An object containing the FX balance information.
    """
    # This is a placeholder implementation. Replace with actual logic to fetch FX balance.
    balance = UserBalanceModel.get(user_id)  # Replace "user_id" with the actual user ID

    return balance.to_fx_balance()


@tool
def order(user_id: str,sell: CurrencyEnum, buy: CurrencyEnum, quantity: int) -> OrderResponse:
    """
    Place an order for the given request.

    Args:
        user_id (str): The user ID placing the order.
        sell (CurrencyEnum): The currency to sell.
        buy (CurrencyEnum): The currency to buy.
        quantity (int): The quantity to order.

    Returns:
        OrderResponse: An object containing the order confirmation or status.
    """
    # This is a placeholder implementation. Replace with actual logic to place an order.
    logger.info(f"Placing order for user: {user_id}", extra={"userId": user_id})
    request = OrderRequest(user_id=user_id, sell=sell, buy=buy, quantity=quantity)



    return exec_order(request)