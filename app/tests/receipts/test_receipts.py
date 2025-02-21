from app.tests.test_helpers import get_jwt, create_receipt


def test_create_receipt_endpoint(test_client, db_session, user_payload, receipt_payload):
    response = create_receipt(user_payload, test_client, receipt_payload)
    assert response.status_code == 200
    assert response.json()["payment"]["type"] == receipt_payload["payment"]["type"]
    assert response.json()["payment"]["amount"] == receipt_payload["payment"]["amount"]


def test_receipts_list(test_client, db_session, user_payload, receipt_payload):
    token = get_jwt(user_payload, test_client)
    create_receipt(user_payload, test_client, receipt_payload)
    response = test_client.get("/receipts/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_receipt_endpoint(test_client, db_session, user_payload, receipt_payload):
    token = get_jwt(user_payload, test_client)
    create_response = create_receipt(user_payload, test_client, receipt_payload)
    receipt_id = create_response.json()["id"]
    
    response = test_client.get(
        f"/receipts/{receipt_id}", 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["id"] == receipt_id


def test_get_receipt_text(test_client, db_session, user_payload, receipt_payload):
    create_response = create_receipt(user_payload, test_client, receipt_payload)
    receipt_id = create_response.json()["id"]

    response = test_client.get(f"/receipts/receipt-txt/{receipt_id}")

    assert response.status_code == 200
    assert "Дякуємо за покупку!" in response.text  
    assert str(receipt_payload["payment"]["amount"]) in response.text  
    assert receipt_payload["products"][0]["name"] in response.text


def test_get_nonexistent_receipt_text(test_client):
    response = test_client.get("/receipts/receipt-txt/999999")  
    assert response.status_code == 404
    assert response.json()["detail"] == "Receipt with id 999999 doesn't exist"


def test_receipt_text_with_custom_width(test_client, db_session, user_payload, receipt_payload):
    create_response = create_receipt(user_payload, test_client, receipt_payload)
    receipt_id = create_response.json()["id"]

    response = test_client.get(f"/receipts/receipt-txt/{receipt_id}?chars_per_line=40")

    assert response.status_code == 200
    assert "=" * 40 in response.text