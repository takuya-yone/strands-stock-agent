import yfinance as yf
from strands import tool

from strands_stock_agent.logger import logger
from strands_stock_agent.schemas import MarketIndexEnum


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
    logger.info(f"Fetching stock information for ticker: {ticker}")
    stock = yf.Ticker(ticker)
    info = stock.info
    return info


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
    logger.info(f"Fetching general market information for market index: {market_index.value}")
    market = yf.Market(market_index.value)

    status = market.status
    return status


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
    logger.info(f"Fetching market summary for market index: {market_index.value}")
    market = yf.Market(market_index.value)
    summary = market.summary
    return summary