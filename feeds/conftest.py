import pytest


@pytest.fixture
def feedparser_data():
    """
    Returns feedparser-like data.
    """
    data = {
        "feed": {"title": "My grandma flirting lessons"},
        "entries": [
            {
                "title": "Approach your pray with a delicious pie",
                "link": "https://my-granda-flirting-lessons.me/1",
                "summary": "awesome content",
                "content": "quality grandma content over here",
            },
            {
                "title": "Wanna feel hot?, wear a sweater",
                "link": "https://my-granda-flirting-lessons.me/2",
                "summary": "awesome content",
                "content": "quality grandma content over here",
            },
            {
                "title": "10 tips to not get asleep on the couch while he is talking",
                "link": "https://my-granda-flirting-lessons.me/3",
                "summary": "awesome content",
                "content": "quality grandma content over here",
            },
        ],
        "status": 200,
    }
    return data
