# tests/test_analysis_router.py
import pytest
from datetime import datetime, timedelta
import requests
from helper import time_and_print_analysis

# Initialize Test Client using requests (SYNCHRONOUS)
@pytest.fixture(scope="module")
def test_client():
    """Return session and close after the tests."""
    session = requests.Session()
    yield session
    session.close()


# Test the /faculty endpoint
def test_get_faculty_analysis_current_month(test_client):
    today = datetime.now().strftime("%Y-%m")
    url = f"/api/analysis/faculty?date={today}"
    time_and_print_analysis(test_client, url, "test_get_faculty_analysis_current_month")


def test_get_faculty_analysis_future_month(test_client):
    url = f"/api/analysis/faculty?date=2025-02"
    time_and_print_analysis(test_client, url, "test_get_faculty_analysis_past_month")


def test_get_faculty_analysis_future_month_faculty(test_client):
    url = f"/api/analysis/faculty?date=2025-01" 
    time_and_print_analysis(test_client, url, "test_get_faculty_analysis_first_month_of_year")

