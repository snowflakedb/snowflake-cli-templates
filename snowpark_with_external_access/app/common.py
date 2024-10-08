import _snowflake
from http.client import HTTPSConnection


def get_secret_value():
    return _snowflake.get_generic_secret_string("generic_secret")


def send_request():
    host = "docs.snowflake.com"
    conn = HTTPSConnection(host)
    conn.request("GET", "/")
    response = conn.getresponse()
    return response.status
