# tests/test_analysis_router.py
import pytest
from datetime import datetime, timedelta
import requests
from helper import time_and_print_analysis
from config import TEST_PAST_DATE, TEST_FACULTY, TEST_BUILDING, TEST_FLOOR


@pytest.fixture(scope="module")
def test_client():
    """Return session and close after the tests."""
    session = requests.Session()
    yield session
    session.close()

# Test the /daily endpoint
def test_get_daily_analysis_current_date(test_client):
    today = datetime.now().strftime("%Y-%m-%d")
    url = f"/api/analysis/daily?date={today}&faculty=&building=&floor="
    time_and_print_analysis(test_client, url, "test_get_daily_analysis_current_date")


def test_get_daily_analysis_past_date(test_client):
    url = f"/api/analysis/daily?date={TEST_PAST_DATE}&faculty=&building=&floor="
    time_and_print_analysis(test_client, url, "test_get_daily_analysis_past_date")


def test_get_daily_analysis_past_date_faculty(test_client):
    faculty_params = f"&faculty={TEST_FACULTY}&building={TEST_BUILDING}&floor={TEST_FLOOR}"
    url = f"/api/analysis/daily?date={TEST_PAST_DATE}{faculty_params}"
    time_and_print_analysis(test_client, url, "test_get_daily_analysis_past_date_faculty")
