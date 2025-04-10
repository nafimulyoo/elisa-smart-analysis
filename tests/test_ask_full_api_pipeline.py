# tests/test_analysis_router.py
import pytest
from datetime import datetime, timedelta
import requests
from tests.helper import time_and_print_ask
from tests.config import ASK_TEST_CASES_WEB, ASK_TEST_CASES_LINE, ASK_TEST_CASES_WHATSAPP

@pytest.fixture(scope="module")
def test_client():
    """Return session and close after the tests."""
    session = requests.Session()
    yield session
    session.close()


@pytest.mark.asyncio    
@pytest.mark.parametrize("question", ASK_TEST_CASES_WEB)
def test_ask_web(test_client, question):
    url = f"/api/web?prompt={question[0]}"
    time_and_print_ask(test_client, url, "test_ask_web")


# @pytest.mark.asyncio
# @pytest.mark.parametrize("question", ASK_TEST_CASES_LINE)
# def test_ask_web(test_client, question):
#     url = f"/api/web/stream?prompt={question}"
#     time_and_print_ask(test_client, url, "test_ask_web")


# @pytest.mark.asyncio
# @pytest.mark.parametrize("question", ASK_TEST_CASES_WHATSAPP)
# def test_ask_web(test_client, question):
#     url = f"/api/web/stream?prompt={question}"
#     time_and_print_ask(test_client, url, "test_ask_web")