from common import get_secret_value, send_request


def request_function() -> str:
    # Retrieve secret value
    _ = get_secret_value()

    # Send request
    return send_request()
