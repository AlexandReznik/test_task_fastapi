def signup_request(user_payload, test_client):
    return test_client.post("user/sign-up/", json=user_payload)


def login_request(user_payload, test_client):
    return test_client.post("user/login/", json=user_payload)


def get_jwt(user_payload, test_client):
    signup_request(user_payload, test_client)
    return login_request(user_payload, test_client).json()["token"]


def create_receipt(user_payload, test_client, receipt_payload):
    token = get_jwt(user_payload, test_client)
    return test_client.post(
        "/receipt/", 
        headers={"Authorization": f"Bearer {token}"}, 
        json=receipt_payload
    )
