# tests/test_analysis_router.py
import pytest
import asyncio
from tests.config import ASK_ANALYSIS_INTERPRETER_TEST_CASES
from mas_llm.roles.analysis_interpreter import AnalysisInterpreter
from tests.helper import prompt_and_result_logger
import pytest

@pytest.mark.asyncio
@pytest.mark.parametrize("question", ASK_ANALYSIS_INTERPRETER_TEST_CASES)
async def test_ask_result_interpreter(question):
    for src in ["web", "line", "whatsapp"]:
        tools = ["fetch_elisa_api_data"]
        if src == "web":
            tools.append("save_csv")
        elif src == "line":
            tools.append("save_plot_image")
        elif src == "whatsapp":
            tools.append("save_plot_image")
    analysis_interpreter = AnalysisInterpreter()
    analysis_interpreter.set_source(src)
    result = await analysis_interpreter.run(question)
    prompt_and_result_logger(question, result, "test_ask_result_interpreter")
    assert result is not None, "Analysis Interpreter result is None"

