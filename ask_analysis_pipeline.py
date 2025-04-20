from fastapi import HTTPException
from model.model import AnalysisResultWeb, AnalysisResultLINE, AnalysisResultWhatsApp
from metagpt.utils.recovery_util import save_history

from mas_llm.actions.handle_initial_prompt import handleInitialPrompt
from mas_llm.actions.interpret_result import InterpretResult
from mas_llm.roles.data_analyst import DataAnalyst

from datetime import datetime

from mas_llm.prompts.write_analysis_code import get_data_analyst_prompt

from tools.tools import fetch_elisa_api_data
from tools.tools import save_csv, save_plot_image
from tools.tools import kmeans_clustering_auto
from loguru import logger as log
from tools.tools import prophet_forecast
import psutil

import nbformat

from metagpt.context import Context
from metagpt.logs import logger

test_response = True

class AskAnalysisPipeline:
    def __init__(self, source, example_mode=False):
        self.source = source
        self.example_mode = example_mode
        self.result = []
        self.progress_callback = None

    async def run(self, message):
            
        if self.example_mode:
            return self.example_output(self.source)
        

        logger.info(f"🎯 Prompt: {message}")
            
        logger.info(f"↗️ Forwarding to Initial Prompt Handler")
        prompt_validator_result = await handleInitialPrompt(message)
            
        logger.info(f"↘️ Prompt Validator result: {prompt_validator_result}")

        if prompt_validator_result.type == "Final Answer" or prompt_validator_result.type == "Unrelevant":
            return self.early_response(prompt_validator_result.message)

        # 40% progress - Setting up tools
        tools = []

        if self.source == "web":
            tools = fetch_elisa_api_data + ["save_csv"]
            print(tools)

        if self.source == "line" or self.source == "whatsapp":
            tools = fetch_elisa_api_data + ["save_plot_image"]

        if prompt_validator_result.type == "Basic Analysis":
            logger.info(f"↗️ Forwarding to Basic Data Analyst")

            react_mode = "react"

        if prompt_validator_result.type == "Advanced Analysis":
            logger.info(f"↗️ Forwarding to Advanced Data Analyst")
            react_mode = "plan_and_act"
            tools += ["k_means_clustering_auto", "prophet_forecast"]
        
        
        data_analyst = DataAnalyst(tools=tools)
        data_analyst.set_react_mode(react_mode=react_mode)

        # initial prompt message 
        data_analyst_requirement = get_data_analyst_prompt(message, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.source)

        await data_analyst.reset_nb()
        logger.warning(f"NOTEBOOK: {data_analyst.execute_code.nb}")
    
        data_analyst_result = await data_analyst.run(data_analyst_requirement)

        save_history(role=data_analyst, save_dir="mas_llm/data/output")

        data_analyst_log = data_analyst.execute_code.nb.copy()

        for cell in data_analyst_log.cells:
            if "outputs" in cell:
                for output in cell["outputs"]:
                    if "data" in output and "image/png" in output["data"]:
                        del output["data"]["image/png"]
        
        # logger.info(f"🟢 Data Analyst result: {data_analyst_log}")
        
        logger.info(f"↗️ Forwarding to Analysis Interpreter")
        logger.info(f"🟢 Analysis Interpreter: Interpreting analysis: {data_analyst_log}")

        interpret_result = InterpretResult()
        analysis_interpreter_result = await interpret_result.run(instruction=f"{data_analyst_log}", source=self.source)
        logger.info(f"🟢 Analysis Interpreter: Interpreting analysis Result: {analysis_interpreter_result}")
        await data_analyst.reset_nb()

        log.remove()
        del interpret_result
        del data_analyst

        print("Killing ipykernel processes...")
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            print(f"Checking process {proc.info['cmdline']} with PID {proc.info['name']}")
            try:
                if isinstance(proc.info['cmdline'], list):
                    proc.info['cmdline'] = ' '.join(proc.info['cmdline'])
                if "ipykernel" in proc.info['cmdline']:
                    print(f"Killing process {proc.info['cmdline']} with PID {proc.info['name']}")
                    proc.kill()
            except:
                pass


        # else:
        #     analysis_interpreter_result = [
        #         {
        #             "data_dir": "data/output/csv/example_one_column_data.csv",
        #             "visualization_type": "bar_chart",
        #             "explanation": "Simple data with bar chart"
        #         },
        #         {
        #             "data_dir": "data/output/csv/example_one_column_data.csv",
        #             "visualization_type": "line_chart",
        #             "explanation": "Simple data with line chart"
        #         },
        #         {
        #             "data_dir": "data/output/csv/example_two_column_data.csv",
        #             "visualization_type": "bar_chart",
        #             "explanation": "Multi data with bar chart"
        #         },
        #         {
        #             "data_dir": "data/output/csv/example_two_column_data.csv",
        #             "visualization_type": "line_chart",
        #             "explanation": "Multi simple data with line chart"
        #         },
        #         {
        #             "data_dir": "data/output/csv/example_cluster_data.csv",
        #             "visualization_type": "scatter_plot",
        #             "explanation": "Cluster data with scatter_plot"
        #         },
        #         {
        #             "data_dir": "data/output/csv/example_very_long_data.csv",
        #             "visualization_type": "",
        #             "explanation": "Very long data (No Chart)"
        #         },
        #         {
        #             "data_dir": "",
        #             "visualization_type": "",
        #             "explanation": "Analysis result with no data"
        #         },
        #     ]
        # logger.info(f"🟢 Analysis Interpreter result: {analysis_interpreter_result}")

        
        
        return analysis_interpreter_result

        
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

    