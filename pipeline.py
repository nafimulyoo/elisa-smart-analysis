from fastapi import HTTPException
from api_model import PromptRequest, AnalysisResultWeb, AnalysisResultLINE, AnalysisResultWhatsApp

from mock.roles.prompt_validator import PromptValidator
from mock.roles.simple_data_analyst import SimpleDataAnalyst
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

        message = request.message
        context = Context()
        logger.info(f"🎯 Prompt: {message}")
        
        prompt_validator = PromptValidator(context=context)
        prompt_validator_result = prompt_validator.run(message)
        logger.info(f"🟢 Prompt validation result: {result}")

        if prompt_validator_result.type == "Final Answer":
            result = [
                AnalysisResultWeb(
                    data={},
                    visualization_type="",
                    explanation=prompt_validator_result.message
                ),
            ]
            return result
        
        if prompt_validator_result.type != "Basic Analysis" and prompt_validator_result.type != "Advanced Analysis":
            logger.error(f"❌ Unknown prompt validation result type: {prompt_validator_result.type}")
            raise HTTPException(status_code=500, detail="Unknown prompt validation result type")

        data_analyst_result = None

        if prompt_validator_result.type == "Basic Analysis":
            logger.info(f"↗️ Forwarding to Simple Data Analyst")
            data_analyst = SimpleDataAnalyst(context=context)
            data_analyst_result = data_analyst.run(message)
            logger.info(f"🟢 Simple Data Analyst result: {data_analyst_result}")

        if prompt_validator_result.type == "Advanced Analysis":
            logger.info(f"↗️ Forwarding to Advanced Data Analyst")
            data_analyst = AdvancedDataAnalyst(context=context)
            data_analyst_result = data_analyst.run(message)
            logger.info(f"🟢 Advanced Data Analyst result: {data_analyst}")
            
            result = data_analyst_result

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

    