# tests/test_analysis_router.py
import pytest
import asyncio
from tests.config import ASK_TEST_CASES_ADVANCED_ANALYSIS, ASK_TEST_CASES_DATE_CONCIOUS, ASK_TEST_CASES_FORECAST, ASK_TEST_CASES_CLUSTERING
from mas_llm.roles.data_analyst import DataAnalyst
from tests.helper import prompt_and_result_logger
from tools.tools import fetch_elisa_api_data
from mas_llm.prompts.write_analysis_code import get_data_analyst_prompt
from datetime import datetime
from metagpt.utils.recovery_util import save_history
import pytest

source = ["web", "line", "whatsapp"]

@pytest.mark.asyncio
@pytest.mark.parametrize("question", ASK_TEST_CASES_ADVANCED_ANALYSIS)
async def test_ask_advanced_analysis(question):
    for src in source:
        tools = fetch_elisa_api_data
        if src == "web":
            tools.append("save_csv")
        elif src == "line":
            tools.append("save_plot_image")
        elif src == "whatsapp":
            tools.append("save_plot_image")

        react_mode = "plan_and_act"
        data_analyst = DataAnalyst(tools=tools)
        data_analyst.set_react_mode(react_mode=react_mode)
        data_analyst_requirement = get_data_analyst_prompt(question, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), src)
        result = await data_analyst.run(data_analyst_requirement)
        prompt_and_result_logger(question, result, f"test_ask_basic_analysis_{src}")
        save_history(role=data_analyst, save_dir="mas_llm/data/test_output")
        data_analyst_log = data_analyst.execute_code.nb

        assert data_analyst_log is not None, "Data Analyst log is None"

    pass


@pytest.mark.asyncio
@pytest.mark.parametrize("question", ASK_TEST_CASES_DATE_CONCIOUS)
async def test_ask_date_concious(question):
    for src in source:
        tools = fetch_elisa_api_data
        if src == "web":
            tools.append("save_csv")
        elif src == "line":
            tools.append("save_plot_image")
        elif src == "whatsapp":
            tools.append("save_plot_image")

        react_mode = "plan_and_act"
        data_analyst = DataAnalyst(tools=tools)
        data_analyst.set_react_mode(react_mode=react_mode)
        data_analyst_requirement = get_data_analyst_prompt(question, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), src)
        result = await data_analyst.run(data_analyst_requirement)
        prompt_and_result_logger(question, result, f"test_ask_basic_analysis_{src}")
        save_history(role=data_analyst, save_dir="mas_llm/data/test_output")
        data_analyst_log = data_analyst.execute_code.nb

        assert data_analyst_log is not None, "Data Analyst log is None"

    pass


@pytest.mark.asyncio
@pytest.mark.parametrize("question", ASK_TEST_CASES_FORECAST)
async def test_ask_forecast(question):
    for src in source:
        tools = fetch_elisa_api_data
        if src == "web":
            tools.append("save_csv")
        elif src == "line":
            tools.append("save_plot_image")
        elif src == "whatsapp":
            tools.append("save_plot_image")

        react_mode = "plan_and_act"
        data_analyst = DataAnalyst(tools=tools)
        data_analyst.set_react_mode(react_mode=react_mode)
        data_analyst_requirement = get_data_analyst_prompt(question, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), src)
        result = await data_analyst.run(data_analyst_requirement)
        prompt_and_result_logger(question, result, f"test_ask_basic_analysis_{src}")
        save_history(role=data_analyst, save_dir="mas_llm/data/test_output")
        data_analyst_log = data_analyst.execute_code.nb

        assert data_analyst_log is not None, "Data Analyst log is None"

    pass


@pytest.mark.asyncio
@pytest.mark.parametrize("question", ASK_TEST_CASES_CLUSTERING)
async def test_ask_clustering(question):
    for src in source:
        tools = fetch_elisa_api_data
        if src == "web":
            tools.append("save_csv")
        elif src == "line":
            tools.append("save_plot_image")
        elif src == "whatsapp":
            tools.append("save_plot_image")

        react_mode = "plan_and_act"
        data_analyst = DataAnalyst(tools=tools)
        data_analyst.set_react_mode(react_mode=react_mode)
        data_analyst_requirement = get_data_analyst_prompt(question, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), src)
        result = await data_analyst.run(data_analyst_requirement)
        prompt_and_result_logger(question, result, f"test_ask_basic_analysis_{src}")
        save_history(role=data_analyst, save_dir="mas_llm/data/test_output")
        data_analyst_log = data_analyst.execute_code.nb

        assert data_analyst_log is not None, "Data Analyst log is None"

    pass