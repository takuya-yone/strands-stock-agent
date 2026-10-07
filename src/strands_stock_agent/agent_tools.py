import yfinance as yf
from strands import tool

from strands_stock_agent.logger import logger
from strands_stock_agent.schemas import FinancialStatementEnum, MarketIndexEnum


@tool
def get_stock_info(ticker:str) -> dict:
    """
    Get stock information for the given ticker symbol.

    Ref. https://ranaroussi.github.io/yfinance/reference/api/yfinance.Ticker.html#yfinance.Ticker

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        dict: A dictionary containing stock information.
    """
    logger.info(f"Fetching stock information for ticker: {ticker}", extra={"ticker": ticker})
    stock = yf.Ticker(ticker)
    return stock.info


@tool
def get_stock_financial_statement(ticker:str, statement: FinancialStatementEnum) -> dict:
    """
    Get the specified financial statement for the given ticker symbol.

    Ref. https://ranaroussi.github.io/yfinance/reference/api/yfinance.Ticker.html#yfinance.Ticker

    Args:
        ticker (str): The stock ticker symbol.
        statement (FinancialStatementEnum): The financial statement to fetch.

    Returns:
        dict: A dictionary containing the requested financial statement information.
    """
    logger.info(f"Fetching {statement.value} for ticker: {ticker}", extra={"ticker": ticker,"statement": statement.value})
    stock = yf.Ticker(ticker)
    if statement == FinancialStatementEnum.BALANCE_SHEET:
        return stock.get_balance_sheet(as_dict=True,pretty=True)
    elif statement == FinancialStatementEnum.INCOME_STATEMENT:
        return stock.get_income_stmt(as_dict=True,pretty=True)
    elif statement == FinancialStatementEnum.CASH_FLOW:
        return stock.get_cash_flow(as_dict=True,pretty=True)
    else:
        logger.error(f"Unsupported financial statement: {statement.value}")
        return {}


@tool
def get_market_status(market_index: MarketIndexEnum) -> dict:
    """
    Get the current status of the specified market index.

    Ref. https://ranaroussi.github.io/yfinance/reference/yfinance.market.html

    Args:
        market_index (MarketIndexEnum): The market index to fetch information for.

    Returns:
        dict: A dictionary containing market information.
    """
    logger.info(f"Fetching general market information for market index: {market_index.value}", extra={"market_index": market_index.value})
    market = yf.Market(market_index.value)

    return market.status


@tool
def get_market_summary(market_index: MarketIndexEnum) -> dict:
    """
    Get the summary information of the specified market index.

    Ref. https://ranaroussi.github.io/yfinance/reference/yfinance.market.html

    Args:
        market_index (MarketIndexEnum): The market index to fetch information for.

    Returns:
        dict: A dictionary containing market summary information.
    """
    logger.info(f"Fetching market summary for market index: {market_index.value}", extra={"market_index": market_index.value})
    market = yf.Market(market_index.value)

    return market.summary