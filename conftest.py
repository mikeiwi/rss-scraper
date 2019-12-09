import pytest
from model_bakery import baker


@pytest.fixture
def authenticated_user(client):
    """
    Returns an authenticated user for the request.
    """
    u = baker.make("User", username="eric")
    u.set_password("coonnfriends")
    u.save()

    client.login(username="eric", password="coonnfriends")
    return u
