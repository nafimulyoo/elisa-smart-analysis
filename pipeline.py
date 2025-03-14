from fastapi import HTTPException
from api_model import PromptRequest, AnalysisResultWeb, AnalysisResultLINE, AnalysisResultWhatsApp

# from mas_llm.roles.initial_prompt_handler import InitialPromptHandler
# from mas_llm.roles.basic_data_analyst import BasicDataAnalyst
# from mas_llm.roles.advanced_data_analyst import AdvancedDataAnalyst
# from mas_llm.roles.analysis_interpreter import AnalysisInterpreter

from mock.roles.initial_prompt_handler import InitialPromptHandler
from mock.roles.basic_data_analyst import BasicDataAnalyst
from mock.roles.advanced_data_analyst import AdvancedDataAnalyst
from mock.roles.analysis_interpreter import AnalysisInterpreter

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
        
        prompt_validator = InitialPromptHandler(context=context)
        prompt_validator_result = await prompt_validator.run(message)

        if prompt_validator_result.type == "Final Answer":
            return self.early_response(prompt_validator_result.message)

        data_analyst_result = None

        if prompt_validator_result.type == "Basic Analysis":
            logger.info(f"↗️ Forwarding to Basic Data Analyst")
            data_analyst = BasicDataAnalyst(context=context)

        if prompt_validator_result.type == "Advanced Analysis":
            logger.info(f"↗️ Forwarding to Advanced Data Analyst")
            data_analyst = AdvancedDataAnalyst(context=context)
            
        data_analyst_result = await data_analyst.run(message)
        logger.info(f"🟢 Data Analyst result: {data_analyst_result}")

        analysis_interpreter = AnalysisInterpreter(context=context, type="web")
        analysis_interpreter_result = analysis_interpreter.run(data_analyst_result)
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

    