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

    @validator("payment_card_first_six")
    @classmethod
    def payment_card_first_six_must_be_6_digits(cls, v: str | None) -> str | None:
        if v and len(v) != 6:
            raise ValueError("must be 6 digits")
        return v

    @validator("payment_card_last_four")
    @classmethod
    def payment_card_last_four_must_be_4_digits(cls, v: str | None) -> str | None:
        if v and len(v) != 4:
            raise ValueError("must be 4 digits")
        return v

    @validator("transaction_id", "payment_card_type", "currency_code", "auth_code")
    @classmethod
    def string_must_not_be_blank(cls, v: str | None) -> str | None:
        """
        Validate that the provided string field is not blank.
        """
        if v is not None and not v.strip():
            raise ValueError("must not be blank")
        return v

    @validator(
        "payment_card_first_six",
        "payment_card_last_four",
        "merchant_identifier",
        "retailer_location_id",
        "items_ordered",
    )
    @classmethod
    def nullify_blank_strings(cls, v: str | None) -> str | None:
        """
        Allow blank strings to be returned as Null in certain cases
        """
        if v is None:
            return v
        null_value: str | None = v.strip()
        if null_value == "":
            null_value = None
        return null_value
