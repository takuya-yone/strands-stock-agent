from pynamodb.attributes import NumberAttribute, UnicodeAttribute
from pynamodb.models import Model

from strands_stock_agent.schemas import FxBalance


class UserBalanceModel(Model):
    """
    A DynamoDB User Balance
    """
    class Meta:
        table_name = "fx-balance-table"
    userId = UnicodeAttribute(hash_key=True)
    JPY = NumberAttribute()
    USD = NumberAttribute()
    EUR = NumberAttribute()
    GBP = NumberAttribute()
    TOTAL_JPY_VALUE = NumberAttribute()

    def to_fx_balance(self) -> FxBalance:
        return FxBalance(
            JPY=self.JPY,
            USD=self.USD,
            EUR=self.EUR,
            GBP=self.GBP
        )


class OrderRecordModel(Model):
    """
    A DynamoDB Order Record
    """
    class Meta:
        table_name = "order-record-table"
    userId = UnicodeAttribute(hash_key=True)
    timestamp = UnicodeAttribute(range_key=True)
    ticker = UnicodeAttribute()
    quantity = NumberAttribute()
    price = NumberAttribute()
    orderId = UnicodeAttribute()
    