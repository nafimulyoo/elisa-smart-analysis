# tests/test_analysis_router.py
import pytest
from datetime import datetime, timedelta
import requests
from helper import time_and_print_analysis
from config import TEST_PAST_MONTH, TEST_FACULTY, TEST_BUILDING, TEST_FLOOR

@pytest.fixture(scope="module")
def test_client():
    """Return session and close after the tests."""
    session = requests.Session()
    yield session
    session.close()

# Test the /monthly endpoint
def test_get_monthly_analysis_current_month(test_client):
    today = datetime.now().strftime("%Y-%m")
    url = f"/api/analysis/monthly?date={today}&faculty=&building=&floor="
    time_and_print_analysis(test_client, url, "test_get_monthly_analysis_current_month")


def test_get_monthly_analysis_past_month(test_client):
    url = f"/api/analysis/monthly?date={TEST_PAST_MONTH}&faculty=&building=&floor="
    time_and_print_analysis(test_client, url, "test_get_monthly_analysis_past_month")


def test_get_monthly_analysis_past_faculty(test_client):
    faculty_params = f"&faculty={TEST_FACULTY}&building={TEST_BUILDING}&floor={TEST_FLOOR}"
    url = f"/api/analysis/monthly?date={TEST_PAST_MONTH}{faculty_params}"
    time_and_print_analysis(test_client, url, "test_get_monthly_analysis_past_month_faculty")
