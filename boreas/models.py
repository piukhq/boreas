"""Models for the Boreas API."""

from __future__ import annotations

from datetime import datetime  # noqa: TCH003

from pydantic import BaseModel, validator


class RetailTransaction(BaseModel):
    """Spec for a Retail Transaction."""

    transaction_id: str
    payment_card_type: str
    payment_card_first_six: str | None
    payment_card_last_four: str | None
    amount: float
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
        """Return a value error if the payment card first six is not 6 digits."""
        if v and len(v) != 6:  # noqa: PLR2004
            msg = "must be 6 digits"
            raise ValueError(msg)
        return v

    @validator("payment_card_last_four")
    @classmethod
    def payment_card_last_four_must_be_4_digits(cls, v: str | None) -> str | None:
        """Return a value error if the payment card first four is not 4 digits."""
        if v and len(v) != 4:  # noqa: PLR2004
            msg = "must be 4 digits"
            raise ValueError(msg)
        return v

    @validator("transaction_id", "payment_card_type", "currency_code", "auth_code")
    @classmethod
    def string_must_not_be_blank(cls, v: str | None) -> str | None:
        """Return a value error if the provided string field is blank."""
        if v is not None and not v.strip():
            msg = "must not be blank"
            raise ValueError(msg)
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
        """Allow blank strings to be returned as Null in certain cases."""
        if v is None:
            return v
        null_value: str | None = v.strip()
        if null_value == "":
            null_value = None
        return null_value
