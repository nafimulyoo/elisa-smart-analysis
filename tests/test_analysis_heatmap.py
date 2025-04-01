# tests/test_analysis_router.py
import pytest
from datetime import datetime, timedelta
import requests
from helper import time_and_print_analysis
from config import TEST_PAST_DATE, TEST_PAST_DATE_END_HEATMAP, TEST_FACULTY, TEST_BUILDING, TEST_FLOOR

@pytest.fixture(scope="module")
def test_client():
    """Return session and close after the tests."""
    session = requests.Session()
    yield session
    session.close()
    
# Test the /heatmap endpoint
def test_get_heatmap_analysis_current_range(test_client):
    today = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d")
    url = f"/api/analysis/heatmap?start={start_date}&end={today}&faculty=&building=&floor="
    time_and_print_analysis(test_client, url, "test_get_heatmap_analysis_valid_range")


def test_get_heatmap_analysis_past_dates(test_client):
    url = f"/api/analysis/heatmap?start=2025-03-01&end=2025-03-07&faculty=&building=&floor="
    time_and_print_analysis(test_client, url, "test_get_heatmap_analysis_past_dates")


def test_get_heatmap_analysis_past_dates_faculty(test_client):
    faculty_params = f"&faculty={TEST_FACULTY}&building={TEST_BUILDING}&floor={TEST_FLOOR}"
    url = f"/api/analysis/heatmap?start={TEST_PAST_DATE}&end={TEST_PAST_DATE_END_HEATMAP}{faculty_params}"
    time_and_print_analysis(test_client, url, "test_get_heatmap_analysis_past_dates_faculty")
