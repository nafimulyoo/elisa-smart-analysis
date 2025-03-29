# tests/test_analysis_router.py
import pytest
from datetime import datetime, timedelta
import requests
from helper import time_and_print_ask
from config import ASK_TEST_CASES_WEB

@pytest.fixture(scope="module")
def test_client():
    """Return session and close after the tests."""
    session = requests.Session()
    yield session
    session.close()
    
@pytest.mark.parametrize("question", ASK_TEST_CASES_WEB)
def test_ask_web(test_client, question):
    url = f"/api/web/stream?prompt={question}"
    time_and_print_ask(test_client, url, "test_ask_web")

# Test the /now endpoint
# def test_ask(test_client):
#     today = datetime.now().strftime("%Y-%m-%d")
#     url = f"/api/analysis/now?date={today}&faculty=&building=&floor="
#     time_and_print(test_client, url, "test_get_now_analysis_current_date")
