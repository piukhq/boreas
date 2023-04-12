from datetime import datetime

from pydantic import BaseModel, validator


class RetailTransaction(BaseModel):
    transaction_id: str
    payment_card_type: str
    payment_card_first_six: str | None
    payment_card_last_four: str | None
    amount: int
    currency_code: str
    auth_code: str
    date: datetime
    merchant_identifier: str | None
    retailer_location_id: str | None
    metadata: dict | None
    items_ordered: str | None

    @classmethod
    @validator("payment_card_first_six")
    def payment_card_first_six_must_be_6_digits(cls, v: str | None):
        if v and len(v) != 6:
            raise ValueError("must be 6 digits")
        return v

    @classmethod
    @validator("payment_card_last_four")
    def payment_card_last_four_must_be_4_digits(cls, v: str | None):
        if v and len(v) != 4:
            raise ValueError("must be 4 digits")
        return v
