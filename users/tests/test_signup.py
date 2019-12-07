"""Users signup testcases"""
import pytest


def test_signup_get_request(client):
    """On GET request, a 200 status code is responded."""
    response = client.get("")
    assert response.status_code == 200
