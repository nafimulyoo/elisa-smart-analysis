import time
import requests
from loguru import logger
from tests.config import TEST_URL
import os

def time_and_print_analysis(session: requests.Session, url, test_name):
    # Create a log file specifically for each test
    log_file_path = f"tests/logs/{test_name}.log"
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    
    logger.add(log_file_path, level="INFO", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

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
        logger.info(f"Result:  {data['analysis']}")
        logger.info(f"Execution time: {execution_time}")
    except requests.RequestException as e:
        logger.error(f"Request error for {test_name}: {e}", url=url)
        assert False, f"Request failed: {e}"
    except Exception as e:
        logger.exception(f"Error processing {test_name}: {e}", url=url)
        assert False, f"Error: {e}"

def time_and_print_ask(session: requests.Session, url, test_name):
    # Create a log file specifically for each test
    # log_file_path = f"tests/logs/{test_name}.log"
    # os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    
    # logger.add(log_file_path, level="DEBUG", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

    start_time = time.perf_counter()
    try:
        # logger.debug(f"Starting request for {test_name} at {url}")
        response = session.get(f"{TEST_URL}{url}")
        end_time = time.perf_counter()
        execution_time = end_time - start_time

        assert response.status_code == 200
        data = response

        # Simple Logging with Loguru
        # logger.info(f"Result:  {data.text}")
        # logger.info(f"Execution time: {execution_time}")

    except requests.RequestException as e:
        # logger.error(f"Request error for {test_name}: {e}", url=url)
        assert False, f"Request failed: {e}"
    except Exception as e:
        # logger.exception(f"Error processing {test_name}: {e}", url=url)
        assert False, f"Error: {e}"
    
    # logger.remove()

def prompt_and_result_logger(prompt, result, test_name):
    # Create a log file specifically for each test
    log_file_path = f"tests/logs/{test_name}.log"
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    
    logger.add(log_file_path, level="DEBUG", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

    logger.debug(f"Prompt: {prompt}")
    logger.debug(f"Result: {result}")
    logger.info("=========================================")
    logger.remove()

def prompt_expected_result_logger(prompt, expected_result, result, test_name):
    # Create a log file specifically for each test
    log_file_path = f"tests/logs/{test_name}.log"
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    
    logger.add(log_file_path, level="DEBUG", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

    logger.info(f"Prompt: {prompt}")
    logger.info(f"Expected Result: {expected_result}")
    if result == expected_result:
        logger.success(f"Result: {result} - Test Passed ✅")
    else:
        logger.error(f"Result: {result} - Test Failed ❌")

    logger.info("=========================================")
    logger.remove()


