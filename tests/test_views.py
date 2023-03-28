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
    assert resp.json() == {"error_message": "Supplied token is invalid", "error_slug": "INVALID_TOKEN"}


@mock.patch("boreas.security.load_secrets", return_value="test-token")
@mock.patch("boreas.views.message_queue.add")
def test_post_malformed_json(mock_queue_add, mock_load_secrets, client, transactions, connection_mock):
    resp = client.post("/retailers/test-retailer/transactions", json="fddfdffd", headers={"x-api-key": "test-token"})
    mock_load_secrets.assert_called_with("test-retailer-transactions-api-key")
    assert not mock_queue_add.called
    assert resp.status_code == 400
    assert resp.json() == {"error_message": "Invalid JSON", "error_slug": "MALFORMED_REQUEST"}
