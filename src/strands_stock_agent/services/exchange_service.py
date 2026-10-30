import yfinance as yf

from strands_stock_agent.db.balance_db import OrderHistoryModel, UserBalanceHistoryModel, UserBalanceModel
from strands_stock_agent.logger import logger
from strands_stock_agent.schemas import (
    CurrencyEnum,
    ExchangeIndexEnum,
    OrderRequest,
    OrderResponse,
)
from strands_stock_agent.services.common import get_timestamp


def exec_order(req: OrderRequest) -> OrderResponse:
    """
    Execute a currency exchange order.

    Args:
        req (OrderRequest): The order request containing user ID, transaction ID, sell currency, buy currency, and quantity.

    Returns:
        OrderResponse: The response containing the transaction ID and timestamp.
    """
    logger.info(
        f"Executing order for user: {req.user_id}, sell: {req.sell}, buy: {req.buy}, buy_quantity: {req.buy_quantity}"
    )

    new_balance = UserBalanceModel.get(req.user_id)

    # buy_quantity is in the buy currency; convert it to the sell currency via JPY

    # if not includes jpy throw error
    if req.sell != CurrencyEnum.JPY and req.buy != CurrencyEnum.JPY:
        raise ValueError("Either sell or buy currency must be JPY")

    sell_quantity = convert_quantity(req.buy_quantity, req.buy, req.sell)
    logger.info(f"Sell quantity: {sell_quantity} {req.sell.value}")

    if req.sell == CurrencyEnum.JPY:
        new_balance.balance.JPY -= sell_quantity
    elif req.sell == CurrencyEnum.USD:
        new_balance.balance.USD -= sell_quantity
    elif req.sell == CurrencyEnum.EUR:
        new_balance.balance.EUR -= sell_quantity
    elif req.sell == CurrencyEnum.GBP:
        new_balance.balance.GBP -= sell_quantity

    # if minus balance, raise an error
    if (
        new_balance.balance.JPY < 0
        or new_balance.balance.USD < 0
        or new_balance.balance.EUR < 0
        or new_balance.balance.GBP < 0
    ):
        raise ValueError("Insufficient balance")

    if req.buy == CurrencyEnum.JPY:
        new_balance.balance.JPY += req.buy_quantity
    elif req.buy == CurrencyEnum.USD:
        new_balance.balance.USD += req.buy_quantity
    elif req.buy == CurrencyEnum.EUR:
        new_balance.balance.EUR += req.buy_quantity
    elif req.buy == CurrencyEnum.GBP:
        new_balance.balance.GBP += req.buy_quantity

    save_balance(req.user_id, new_balance, req.transaction_id)
    save_user_balance_history(req.user_id, new_balance, req.transaction_id)
    save_order_history(
        req.user_id,
        req.transaction_id,
        f"{req.sell.value}/{req.buy.value}",
        req.buy_quantity,
        get_jpy_rate(req.buy),
    )

    res = OrderResponse(transaction_id=req.transaction_id)
    return res


def save_order_history(user_id: str, transaction_id: str, ticker: str, quantity: float, price: float):
    """
    Save the order history to the database.

    Args:
        user_id (str): The user ID associated with the order.
        transaction_id (str): The transaction ID for the order.
        ticker (str): The ticker symbol of the asset.
        quantity (float): The quantity of the asset.
        price (float): The price of the asset.
    """
    logger.info(f"Saving order history for user_id={user_id}, transaction_id={transaction_id}")
    _timestamp = get_timestamp()
    history = OrderHistoryModel(
        transactionId=transaction_id,
        userId=user_id,
        timestamp=_timestamp,
        ticker=ticker,
        quantity=quantity,
        price=price,
    )
    history.save()
    logger.info(f"Order history created: {history.transactionId}")


def save_user_balance_history(user_id: str, new_balance: UserBalanceModel, transaction_id: str):
    """
    Save the user's balance history to the database.

    Args:
        user_id (str): The user ID for which to save the balance history.
        new_balance (UserBalanceModel): The current balance object.
        transaction_id (str): The transaction ID associated with this balance update.
        timestamp (str): The timestamp of the balance snapshot.
    """
    logger.info(f"Saving user balance history for user_id={user_id}, transaction_id={transaction_id}")
    timestamp = get_timestamp()
    history = UserBalanceHistoryModel(
        userId=user_id,
        timestamp=timestamp,
        transactionId=transaction_id,
        balance={
            "JPY": new_balance.balance.JPY,
            "USD": new_balance.balance.USD,
            "EUR": new_balance.balance.EUR,
            "GBP": new_balance.balance.GBP,
        },
        totalJpyValue=calc_jpy_value(new_balance),
    )
    history.save()


def get_jpy_rate(currency: CurrencyEnum) -> float:
    """
    Get the JPY value of one unit of the given currency.

    Args:
        currency (CurrencyEnum): The currency to look up.

    Returns:
        float: JPY per one unit of the currency (1.0 for JPY).
    """
    if currency == CurrencyEnum.JPY:
        return 1.0
    return get_last_price(ExchangeIndexEnum[f"{currency.value}JPY"])


def convert_quantity(quantity: float, from_currency: CurrencyEnum, to_currency: CurrencyEnum) -> float:
    """
    Convert an amount from one currency to another via JPY.

    Args:
        quantity (float): The amount in from_currency.
        from_currency (CurrencyEnum): The currency of the amount.
        to_currency (CurrencyEnum): The currency to convert to.

    Returns:
        float: The equivalent amount in to_currency.
    """
    if from_currency == to_currency:
        return quantity
    return quantity * get_jpy_rate(from_currency) / get_jpy_rate(to_currency)


def save_balance(user_id: str, new_balance: UserBalanceModel, transaction_id: str):
    """
    Save the updated user balance to the database.

    Args:
        user_id (str): The user ID for which to save the balance.
        new_balance (UserBalanceModel): The updated balance object.
        transaction_id (str): The transaction ID associated with this balance update.
    """
    logger.info(f"Saving user balance for user_id={user_id}, transaction_id={transaction_id}")
    balance = UserBalanceModel.get(user_id)
    balance.balance.JPY = new_balance.balance.JPY
    balance.balance.USD = new_balance.balance.USD
    balance.balance.EUR = new_balance.balance.EUR
    balance.balance.GBP = new_balance.balance.GBP
    balance.latestTransactionId = transaction_id
    balance.totalJpyValue = calc_jpy_value(new_balance)
    balance.save()


def calc_jpy_value(balance: UserBalanceModel):
    """
    Calculate the total value of the user's balance in JPY.

    Args:
        balance (UserBalanceModel): The user's balance object.

    Returns:
        int: The total value of the balance in JPY.
    """
    jpy_value = balance.balance.JPY

    jpy_value += balance.balance.USD * get_last_price(ExchangeIndexEnum.USDJPY)
    jpy_value += balance.balance.EUR * get_last_price(ExchangeIndexEnum.EURJPY)
    jpy_value += balance.balance.GBP * get_last_price(ExchangeIndexEnum.GBPJPY)

    return int(jpy_value)


def get_last_price(ticker: ExchangeIndexEnum) -> float:
    """
    Get the last price for the given exchange ticker.

    Args:
        ticker (ExchangeIndexEnum): The exchange ticker symbol.

    Returns:
        float: The last price of the exchange ticker.
    """
    exchange = yf.Ticker(ticker.value).fast_info["lastPrice"]
    return exchange
