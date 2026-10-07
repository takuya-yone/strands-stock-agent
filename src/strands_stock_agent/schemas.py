from enum import Enum


class MarketIndexEnum(Enum):
    US = "US"
    GB = "GB"
    ASIA = "ASIA"
    EUROPE = "EUROPE"
    RATES = "RATES"
    COMMODITIES = "COMMODITIES"
    CURRENCIES = "CURRENCIES"
    CRYPTOCURRENCIES = "CRYPTOCURRENCIES"



class FinancialStatementEnum(Enum):
    BALANCE_SHEET = "BALANCE_SHEET"
    INCOME_STATEMENT = "INCOME_STATEMENT"
    CASH_FLOW = "CASH_FLOW"