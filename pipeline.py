from fastapi import HTTPException
from api_model import PromptRequest, AnalysisResultWeb, AnalysisResultLINE, AnalysisResultWhatsApp
from metagpt.utils.recovery_util import save_history

from mas_llm.roles.initial_prompt_handler import InitialPromptHandler
from mas_llm.roles.data_analyst import DataAnalyst
from mas_llm.roles.analysis_interpreter import AnalysisInterpreter

from datetime import datetime

from mas_llm.prompts.write_analysis_code import get_data_analyst_prompt

from tools import fetch_elisa_api_data
from tools import save_csv, save_plot_image
from tools import kmeans_clustering_auto
from tools import prophet_forecast

# from mock.roles.initial_prompt_handler import InitialPromptHandler
# from mock.roles.basic_data_analyst import BasicDataAnalyst
# from mock.roles.advanced_data_analyst import AdvancedDataAnalyst
# from mock.roles.analysis_interpreter import AnalysisInterpreter

from metagpt.context import Context
from metagpt.logs import logger

class Pipeline:
    def __init__(self, source, example_mode=False):
        self.source = source
        self.example_mode = example_mode
        self.result = []

    async def run(self, request):
        if self.example_mode:
            return self.example_output(self.source)

        message = request.prompt
        context = Context()
        logger.info(f"🎯 Prompt: {message}")
        
        logger.info(f"↗️ Forwarding to Initial Prompt Handler")
        prompt_validator = InitialPromptHandler(context=context)
        prompt_validator_result = await prompt_validator.run(message)

        logger.info(f"↘️ Prompt Validator result: {prompt_validator_result}")

        if prompt_validator_result.type == "Final Answer":
            return self.early_response(prompt_validator_result.message)

        tools = fetch_elisa_api_data

        if self.source == "web":
            tools.append("save_csv")
            print(tools)

        if self.source == "line" or self.source == "whatsapp":
            tools.append("save_plot_image")

        if prompt_validator_result.type == "Basic Analysis":
            logger.info(f"↗️ Forwarding to Basic Data Analyst")
            # react_mode = "plan_and_act"
            react_mode = "react"

        if prompt_validator_result.type == "Advanced Analysis":
            logger.info(f"↗️ Forwarding to Advanced Data Analyst")
            react_mode = "plan_and_act"
            tools += ["k_means_clustering_auto", "prophet_forecast"]
            
        data_analyst = DataAnalyst(tools=tools)
        data_analyst.set_react_mode(react_mode=react_mode)
        
        data_analyst_requirement = get_data_analyst_prompt(prompt_validator_result.message, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.source)

        data_analyst_result = await data_analyst.run(data_analyst_requirement)

        save_history(role=data_analyst, save_dir="mas_llm/data/output")

        data_analyst_log = data_analyst.execute_code.nb

        for cell in data_analyst_log.cells:
            if "outputs" in cell:
                for output in cell["outputs"]:
                    if "data" in output and "image/png" in output["data"]:
                        del output["data"]["image/png"]
        
        logger.info(f"🟢 Data Analyst result: {data_analyst_log}")

        analysis_interpreter = AnalysisInterpreter(context=context)
        analysis_interpreter.set_source(self.source)
        
        logger.info(f"↗️ Forwarding to Analysis Interpreter")

        analysis_interpreter_result = await analysis_interpreter.run(f"{data_analyst_log}")
        logger.info(f"🟢 Analysis Interpreter result: {analysis_interpreter_result}")

        return analysis_interpreter_result

    def example_output(self, type):
        if type == "web":
            result = [
                AnalysisResultWeb(
                    data={"example_key": "example_value"},
                    visualization_type="bar_chart",
                    explanation="1. This is an example explanation for the analysis."
                ),
                AnalysisResultWeb(
                    data={"example_key": "example_value"},
                    visualization_type="line_chart",
                    explanation="2. This is an example explanation for the analysis."
                ),
            ]
            return result
        elif type == "line":
            result = [
                AnalysisResultLINE(
                    image_url="https://example.com/image.png",
                    explanation="1. This is an example explanation for the LINE analysis."
                ),
                AnalysisResultLINE(
                    image_url="https://example.com/image.png",
                    explanation="2. This is an example explanation for the LINE analysis."
                )
            ]
            return result

        elif type == "whatsapp":
            result = [
                AnalysisResultWhatsApp(
                    image_url="https://example.com/image.png",
                    explanation="1. This is an example explanation for the WhatsApp analysis."
                ),
                AnalysisResultWhatsApp(
                    image_url="https://example.com/image.png",
                    explanation="2. This is an example explanation for the WhatsApp analysis."
                )
            ]
            return result
        else :
            logger.error(f"❌ Unknown source type: {type}")
            raise HTTPException(status_code=500, detail="Unknown source type")
        
    def early_response(self, message):
        if self.source == "web":
            return [AnalysisResultWeb(data={}, visualization_type="", explanation=message)]
        elif self.source == "line":
            return [AnalysisResultLINE(image_url="", explanation=message)]
        elif self.source == "whatsapp":
            return [AnalysisResultWhatsApp(image_url="", explanation=message)]

    