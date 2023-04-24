from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from boreas.app import create_app


@pytest.fixture()
def client():
    app = create_app()
    yield TestClient(app)


@pytest.fixture()
def connection_mock():
    return Mock()


@pytest.fixture()
def transactions():
    yield [
        {
            "transaction_id": "QTZENTY0DdGOEJCQkU3",
            "payment_card_type": "visa",
            "payment_card_first_six": "454546",
            "payment_card_last_four": "6309",
            "amount": 23.99,
            "currency_code": "GBP",
            "auth_code": "188328",
            "date": "2023-01-30T11:14:34+00:00",
            "merchant_identifier": "10209723",
            "retailer_location_id": "store_1a",
            "metadata": {},
            "items_ordered": '{"products":[{"id":"2","productUuid":"534084a0-a6a3-11ec-b020-211a45f43f11",'
            '"variantUuid":"5341e430-a6a3-11ec-a1a4-0f05978902ad","description":"","name":'
            '"Test product 1","sku":"sku1","unitPrice":30,"costPrice":10,"quantity":"2",'
            '"vatPercentage":0.0,"taxRates":[{"percentage":0}],"taxExempt":false,"autoGenerated"'
            ':false,"type":"PRODUCT"},{"id":"3","productUuid":"6afeb440-a6a3-11ec-8cbe-3d86e849bdc6",'
            '"variantUuid":"6affc5b0-a6a3-11ec-8fa7-064bffdcf323","description":"",'
            '"name":"Test product 2","sku":"sku22","unitPrice":40,"costPrice":0,"quantity":"1",'
            '"vatPercentage":0.0,"taxRates":[{"percentage":0}],"taxExempt":false,'
            '"autoGenerated":false,"type":"PRODUCT"}]}',
        }
    ]
