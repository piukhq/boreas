import typing
from unittest import mock


@mock.patch("boreas.security.load_secrets", return_value="test-token")
@mock.patch("boreas.views.message_queue.add")
def test_post_200(mock_queue_add, mock_load_secrets, client, transactions, connection_mock):
    resp = client.post("/retailers/test-retailer/transactions", json=transactions, headers={"x-api-key": "test-token"})
    mock_load_secrets.assert_called_with("test-retailer-transactions-api-key")
    assert mock_queue_add.called
    assert resp.status_code == 200


@mock.patch("boreas.security.load_secrets", return_value="test-token")
@mock.patch("boreas.views.message_queue.add")
def test_post_failed_auth(mock_queue_add, mock_load_secrets, client, transactions, connection_mock):
    resp = client.post("/retailers/test-retailer/transactions", json=transactions, headers={"x-api-key": "wrong-key"})
    mock_load_secrets.assert_called_with("test-retailer-transactions-api-key")
    assert not mock_queue_add.called
    assert resp.status_code == 401
    assert resp.json() == {
        "detail": [
            {
                "msg": "Authentication failed",
                "type": "Unauthorized",
            }
        ]
    }


@mock.patch("boreas.security.load_secrets", return_value="test-token")
@mock.patch("boreas.views.message_queue.add")
def test_post_malformed_json(mock_queue_add, mock_load_secrets, client, transactions, connection_mock):
    resp = client.post("/retailers/test-retailer/transactions", json="fddfdffd", headers={"x-api-key": "test-token"})
    mock_load_secrets.assert_called_with("test-retailer-transactions-api-key")
    assert not mock_queue_add.called
    assert resp.status_code == 422
    assert resp.json() == {
        "detail": [
            {
                "type": "list_type",
                "loc": ["body"],
                "msg": "Input should be a valid list",
                "input": "fddfdffd",
                "url": mock.ANY,
            }
        ]
    }
    url = resp.json()["detail"][0]["url"]
    assert url[:28] + url[31:] == "https://errors.pydantic.dev//v/list_type"
    assert float(url[28:31])
