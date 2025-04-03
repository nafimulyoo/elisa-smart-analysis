# tests/test_analysis_router.py
import pytest
#
import asyncio
from tests.config import ASK_TEST_CASES_BASIC_KNOWLEDGE,  ASK_TEST_CASES_BASIC_KNOWLEDGE, ASK_TEST_CASES_UNRELEVANT, ASK_TEST_CASES_DATA_AVAILABILITY
from mas_llm.roles.initial_prompt_handler import RespondInitialPrompt, AskAboutElisa
from tests.helper import prompt_expected_result_logger, prompt_and_result_logger
import pytest
#

@pytest.mark.parametrize("question", ASK_TEST_CASES_BASIC_KNOWLEDGE)
def test_ask_respond_initial_prompt(question):
    respond_initial_prompt = RespondInitialPrompt()
    result = asyncio.run(respond_initial_prompt.run(question[0]))
    prompt_expected_result_logger(question[0], question[1], result.type, "test_ask_respond_initial_prompt")
    assert result.type == question[1]


@pytest.mark.parametrize("question", ASK_TEST_CASES_BASIC_KNOWLEDGE)
def test_basic_knowledge(question):
    ask_about_elisa = AskAboutElisa()
    result = asyncio.run(ask_about_elisa.run(question[0]))
    prompt_and_result_logger(question, result, "test_basic_knowledge")


@pytest.mark.parametrize("question", ASK_TEST_CASES_UNRELEVANT)
def test_unrelevant(question):
    ask_about_elisa = AskAboutElisa()
    result = asyncio.run(ask_about_elisa.run(question[0]))
    prompt_and_result_logger(question, result, "test_unrelevant")

@pytest.mark.parametrize("question", ASK_TEST_CASES_DATA_AVAILABILITY)
def test_data_availability(question):
    ask_about_elisa = AskAboutElisa()
    result = asyncio.run(ask_about_elisa.run(question[0]))
    prompt_and_result_logger(question, result, "test_data_availability")
