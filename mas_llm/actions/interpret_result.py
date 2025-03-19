from api_model import InitialPromptHandlerResult
from mas_llm.prompts.interpret_result import INTERPRET_RESULT_WEB_PROMPT, INTERPRET_RESULT_LINE_PROMPT, INTERPRET_RESULT_WHATSAPP_PROMPT
import re
from metagpt.actions import Action
import json
from metagpt.logs import logger

class InterpretResult(Action):
    name: str = "InterpretResult"
    async def run(self, instruction: str, source: str):
        image_pattern = r"'image/png': \'.*?\'"
        instruction_filtered = re.sub(image_pattern, "", instruction)

        logger.info(f"🟢 InterpretResult Instruction: {instruction_filtered}")
        prompt = ""
        if source == "web":
            prompt = INTERPRET_RESULT_WEB_PROMPT.format(instruction=instruction_filtered)
        if source == "line":
            prompt = INTERPRET_RESULT_LINE_PROMPT.format(instruction=instruction_filtered)
        if source == "whatsapp":
            prompt = INTERPRET_RESULT_WHATSAPP_PROMPT.format(instruction=instruction_filtered)

        response = await self._aask(prompt)

        result = self.parse_json(response)

        return result

    @staticmethod
    def parse_json(response):
        pattern = r"```json(.*)```"
        match = re.search(pattern, response, re.DOTALL)
        
        json_string = match.group(1) if match else response

        json_object = json.loads(json_string)

        return json_object
    