from fastapi import HTTPException
from api_model import AnalysisResultWeb, AnalysisResultLINE, AnalysisResultWhatsApp
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

from metagpt.context import Context
from metagpt.logs import logger


class AskAnalysisPipeline:
    def __init__(self, source, example_mode=False):
        self.source = source
        self.example_mode = example_mode
        self.result = []
        self.progress_callback = None

    async def set_progress_callback(self, callback):
        """Set a callback to report progress"""
        self.progress_callback = callback

    async def update_progress(self, progress, message):
        """Update the progress if a callback is set"""
        if self.progress_callback:
            # await self.progress_callback(progress, message)
            self.progress_callback(progress, message)

    async def run(self, message):
        if self.example_mode:
            return self.example_output(self.source)

        context = Context()
        logger.info(f"🎯 Prompt: {message}")
        
        # Initial prompt handling - 20% progress
        await self.update_progress(20, "Analyzing request...")
        logger.info(f"↗️ Forwarding to Initial Prompt Handler")
        prompt_validator = InitialPromptHandler(context=context)
        prompt_validator_result = await prompt_validator.run(message)
        
        logger.info(f"↘️ Prompt Validator result: {prompt_validator_result}")

        if prompt_validator_result.type == "Final Answer" or prompt_validator_result.type == "Unrelevant":
            await self.update_progress(50, "Answering question...")
            return self.early_response(prompt_validator_result.message)

        # 40% progress - Setting up tools
        await self.update_progress(40, "Fetching data...")
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
        
        # 60% progress - Data analysis    
        await self.update_progress(60, "Analyzing data...")
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

        # 80% progress - Interpreting results
        await self.update_progress(80, "Interpreting results...")
        analysis_interpreter = AnalysisInterpreter(context=context)
        analysis_interpreter.set_source(self.source)
        
        logger.info(f"↗️ Forwarding to Analysis Interpreter")

        analysis_interpreter_result = await analysis_interpreter.run(f"{data_analyst_log}")
        logger.info(f"🟢 Analysis Interpreter result: {analysis_interpreter_result}")

        # 100% progress - Completed
        await self.update_progress(100, "Finalization...")
        
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
            return [{
                "data_dir": "",
                "visualization_type": "",
                "explanation": message
            }]
        elif self.source == "line":
            return [{
                "image_dir": "",
                "explanation": message
            }]
        elif self.source == "whatsapp":
            return [{
                "image_dir": "",
                "explanation": message
            }]

    