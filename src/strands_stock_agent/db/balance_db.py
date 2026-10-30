from pynamodb.attributes import MapAttribute, NumberAttribute, UnicodeAttribute
from pynamodb.models import Model

from strands_stock_agent.schemas import FxBalance


class UserBalanceModel(Model):
    """
    A DynamoDB User Balance
    """

    class Meta:
        table_name = "fx-balance-table"

    userId = UnicodeAttribute(hash_key=True)
    balance = MapAttribute(JPY=NumberAttribute(), USD=NumberAttribute(), EUR=NumberAttribute(), GBP=NumberAttribute())
    latestTransactionId = UnicodeAttribute(null=True)

    def to_fx_balance(self) -> FxBalance:
        return FxBalance(JPY=self.balance.JPY, USD=self.balance.USD, EUR=self.balance.EUR, GBP=self.balance.GBP)


class UserBalanceHistoryModel(Model):
    """
    A DynamoDB User Balance History
    """

    class Meta:
        table_name = "fx-balance-history-table"

    userId = UnicodeAttribute(hash_key=True)
    timestamp = UnicodeAttribute(range_key=True)
    transactionId = UnicodeAttribute()
    balance = MapAttribute(JPY=NumberAttribute(), USD=NumberAttribute(), EUR=NumberAttribute(), GBP=NumberAttribute())
    totalJpyValue = NumberAttribute()


class OrderHistoryModel(Model):
    """
    A DynamoDB Order History
    """

    class Meta:
        table_name = "fx-order-history-table"

    userId = UnicodeAttribute(hash_key=True)
    timestamp = UnicodeAttribute(range_key=True)
    transactionId = UnicodeAttribute()
    ticker = UnicodeAttribute()
    quantity = NumberAttribute()
    price = NumberAttribute()
