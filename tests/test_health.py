# tests/test_analysis_router.py
import pytest
from datetime import datetime, timedelta
import os
import requests
import time

TEST_URL = "http://localhost:8000"

# Initialize Test Client using requests (SYNCHRONOUS)
@pytest.fixture(scope="module")
def test_client():
    """Return session and close after the tests."""
    session = requests.Session()
    yield session
    session.close()


def test_health_self(test_client):
    start_time = time.perf_counter()
    try:
        response = test_client.get(f"{TEST_URL}/health")
        end_time = time.perf_counter()
        execution_time = end_time - start_time

        assert response.status_code == 200
        data = response.json()
        assert data == {"status": "OK"}
        print(f"test_health_check execution time: {execution_time:.4f} seconds")
    except requests.RequestException as e:
        print(f"Request error for test_health_check: {e}")
        assert False, f"Request failed: {e}"
    except Exception as e:
        print(f"Error processing test_health_check: {e}")
        assert False, f"Error: {e}"

def test_health_elisa(test_client):
    start_time = time.perf_counter()
    try:
        response = test_client.get(f"{TEST_URL}/health?object=elisa")
        end_time = time.perf_counter()
        execution_time = end_time - start_time

        assert response.status_code == 200
        data = response.json()
        assert data == {"status": "OK"}
        print(f"test_health_check_elisa execution time: {execution_time:.4f} seconds")
    except requests.RequestException as e:
        print(f"Request error for test_health_check_elisa: {e}")
        assert False, f"Request failed: {e}"
    except Exception as e:
        print(f"Error processing test_health_check_elisa: {e}")
        assert False, f"Error: {e}"