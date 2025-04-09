# tests/test_analysis_router.py
import pytest
#
import asyncio
from tests.config import ASK_TEST_CASES_BASIC_ANALYSIS
from mas_llm.roles.data_analyst import DataAnalyst
from tests.helper import prompt_expected_result_logger, prompt_and_result_logger
from tools import fetch_elisa_api_data
from mas_llm.prompts.write_analysis_code import get_data_analyst_prompt
from datetime import datetime
from metagpt.utils.recovery_util import save_history

import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize("question", ASK_TEST_CASES_BASIC_ANALYSIS)
async def test_ask_basic_analysis_web(question):
    tools = fetch_elisa_api_data
    tools.append("save_csv")
    react_mode = "react"

    data_analyst = DataAnalyst(tools=tools)
    data_analyst.set_react_mode(react_mode=react_mode)

    data_analyst_requirement = get_data_analyst_prompt(question, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "web")

    result = await data_analyst.run(data_analyst_requirement)

    prompt_and_result_logger(question, result, "test_ask_basic_analysis_web")

    save_history(role=data_analyst, save_dir="mas_llm/data/test_output")
    
    data_analyst_log = data_analyst.execute_code.nb
    assert data_analyst_log is not None, "Data Analyst log is None"
    pass


# @pytest.mark.asyncio
# @pytest.mark.parametrize("question", ASK_TEST_CASES_BASIC_ANALYSIS)
# async def test_ask_basic_analysis_line(question):
#     tools = fetch_elisa_api_data
#     tools.append("save_plot_image")
#     react_mode = "react"

#     data_analyst = DataAnalyst(tools=tools)
#     data_analyst.set_react_mode(react_mode=react_mode)

#     data_analyst_requirement = get_data_analyst_prompt(question, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "line")

#     result = await data_analyst.run(data_analyst_requirement)

#     prompt_and_result_logger(question, result, "test_ask_basic_analysis_line")

#     save_history(role=data_analyst, save_dir="mas_llm/data/test_output")
    
#     data_analyst_log = data_analyst.execute_code.nb
#     assert data_analyst_log is not None, "Data Analyst log is None"


# @pytest.mark.asyncio
# @pytest.mark.parametrize("question", ASK_TEST_CASES_BASIC_ANALYSIS)
# async def test_ask_basic_analysis_whatsapp(question):
#     tools = fetch_elisa_api_data
#     tools.append("save_plot_image")
#     react_mode = "react"

#     data_analyst = DataAnalyst(tools=tools)
#     data_analyst.set_react_mode(react_mode=react_mode)

#     data_analyst_requirement = get_data_analyst_prompt(question, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "whatsapp")

#     result = await data_analyst.run(data_analyst_requirement)

#     prompt_and_result_logger(question, result, "test_ask_basic_analysis_whatsapp")

#     save_history(role=data_analyst, save_dir="mas_llm/data/test_output")
    
#     data_analyst_log = data_analyst.execute_code.nb
#     assert data_analyst_log is not None, "Data Analyst log is None"
