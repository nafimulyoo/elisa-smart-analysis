from model.model import InitialPromptHandlerResult
import re
from metagpt.actions import Action
import json

from mas_llm.prompts.initial_prompt import ASK_DATA_PROMPT
from metagpt.rag.engines import SimpleEngine
from metagpt.rag.schema import BM25RetrieverConfig, LLMRankerConfig

DOC_PATH = "mas_llm/rag/data/elisa/data_availability.txt"

class AskDataAvailability(Action):

    name: str = "AskDataAvailability"

    async def run(self, instruction: str):
        prompt = ASK_DATA_PROMPT.format(instruction=instruction)

        engine = SimpleEngine.from_docs(
            input_files=[DOC_PATH],
            retriever_configs=[BM25RetrieverConfig()]
        )

        response = await engine.aquery(prompt)
        
        result = self.parse_json(response.response)

        return result

    @staticmethod
    def parse_json(response):
        pattern = r"```json(.*)```"
        match = re.search(pattern, response, re.DOTALL)
        
        json_string = match.group(1) if match else response

        json_object = json.loads(json_string)

        result = InitialPromptHandlerResult(
            type=json_object.get("type"),
            message=json_object.get("message")
        )

        return result
    