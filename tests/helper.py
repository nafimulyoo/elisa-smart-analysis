import time
import requests
from loguru import logger
from config import TEST_URL
import os

def time_and_print(session: requests.Session, url, test_name):
    # Create a log file specifically for each test
    log_file_path = f"tests/logs/{test_name}.log"
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    logger.info("\n\n")
    logger.add(log_file_path, level="DEBUG", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

    start_time = time.perf_counter()
    try:
        logger.debug(f"Starting request for {test_name} at {url}")
        response = session.get(f"{TEST_URL}{url}")
        end_time = time.perf_counter()
        execution_time = end_time - start_time

        assert response.status_code == 200
        data = response.json()
        assert "analysis" in data

        # Simple Logging with Loguru
        logger.info(
            f"{test_name} COMPLETED",
            execution_time=execution_time,
            result=data['analysis'],
            url=url,
            status_code=response.status_code,
        )
        logger.success(f"Execution time: {execution_time}")
        logger.success(f"Result:  {data['analysis']}")
    except requests.RequestException as e:
        logger.error(f"Request error for {test_name}: {e}", url=url)
        assert False, f"Request failed: {e}"
    except Exception as e:
        logger.exception(f"Error processing {test_name}: {e}", url=url)
        assert False, f"Error: {e}"

    logger.remove()