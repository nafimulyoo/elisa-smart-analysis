from api_model import InitialPromptHandlerResult
from mas_llm.prompts.initial_prompt import INITIAL_PROMPT
import re
from metagpt.actions import Action
import json

class RespondInitialPrompt(Action):
    name: str = "RespondInitialPrompt"

    async def run(self, instruction: str):
        prompt = INITIAL_PROMPT.format(instruction=instruction)

        response = await self._aask(prompt)

        result = self.parse_json(response)

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
    