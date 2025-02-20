from app.tests.test_helpers import get_jwt, create_receipt


def test_create_receipt_endpoint(test_client, db_session, user_payload, receipt_payload):
    response = create_receipt(user_payload, test_client, receipt_payload)
    assert response.status_code == 200
    assert response.json()["payment"]["type"] == receipt_payload["payment"]["type"]
    assert response.json()["payment"]["amount"] == receipt_payload["payment"]["amount"]


def test_receipts_list(test_client, db_session, user_payload, receipt_payload):
    token = get_jwt(user_payload, test_client)
    create_receipt(user_payload, test_client, receipt_payload)
    response = test_client.get("/receipt/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_receipt_endpoint(test_client, db_session, user_payload, receipt_payload):
    token = get_jwt(user_payload, test_client)
    create_response = create_receipt(user_payload, test_client, receipt_payload)
    receipt_id = create_response.json()["id"]
    
    response = test_client.get(
        f"/receipt/{receipt_id}", 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["id"] == receipt_id
