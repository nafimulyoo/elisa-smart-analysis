# tests/test_analysis_router.py
import pytest
import asyncio
from tests.config import ASK_TEST_CASES_BASIC_KNOWLEDGE, ASK_TEST_CASES_UNRELEVANT, ASK_TEST_CASES_DATA_AVAILABILITY, ASK_TEST_CASES_RESPOND_INITIAL_PROMPT
from mas_llm.roles.initial_prompt_handler import RespondInitialPrompt, AskAboutElisa, AskDataAvailability
from tests.helper import prompt_expected_result_logger, prompt_and_result_logger
import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize("question", ASK_TEST_CASES_RESPOND_INITIAL_PROMPT)
async def test_ask_respond_initial_prompt(question):
    respond_initial_prompt = RespondInitialPrompt()
    result = await respond_initial_prompt.run(question[0])
    prompt_expected_result_logger(question[0], question[1], result.type, "test_ask_respond_initial_prompt")
    assert result.type == question[1]


@pytest.mark.asyncio
@pytest.mark.parametrize("question", ASK_TEST_CASES_BASIC_KNOWLEDGE)
async def test_basic_knowledge(question):
    ask_about_elisa = AskAboutElisa()
    result = await ask_about_elisa.run(question)
    prompt_and_result_logger(question, result, "test_basic_knowledge")


@pytest.mark.asyncio
@pytest.mark.parametrize("question", ASK_TEST_CASES_UNRELEVANT)
async def test_unrelevant(question):
    respond_initial_prompt = RespondInitialPrompt()
    result = await respond_initial_prompt.run(question)
    prompt_and_result_logger(question, f"Type: {result.type}, Message: {result.message}", "test_unrelevant")
    assert result.type == "Unrelevant"


@pytest.mark.asyncio
@pytest.mark.parametrize("question", ASK_TEST_CASES_DATA_AVAILABILITY)
async def test_data_availability(question):
    ask_data_availability = AskDataAvailability()
    result = await ask_data_availability.run(question[0])
    prompt_expected_result_logger(question[0], question[1], result.type, "test_data_availability")
    assert result.type == question[1]

