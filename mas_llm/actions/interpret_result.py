from mas_llm.prompts.interpret_result import INTERPRET_RESULT_WEB_PROMPT, INTERPRET_RESULT_LINE_PROMPT, INTERPRET_RESULT_WHATSAPP_PROMPT
import re
from metagpt.actions import Action
import json
from metagpt.logs import logger

class InterpretResult(Action):
    name: str = "InterpretResult"
    async def run(self, notebook: str, question: str, source: str):
        image_pattern = r"'image/png': \'.*?\'"
        notebook_filtered = re.sub(image_pattern, "", notebook)

        # logger.info(f"🟢 InterpretResult Instruction: {instruction_filtered}")
        prompt = ""
        if source == "web":
            prompt = INTERPRET_RESULT_WEB_PROMPT.format(notebook=notebook_filtered, question=question)
        if source == "line":
            prompt = INTERPRET_RESULT_LINE_PROMPT.format(notebook=notebook_filtered, question=question)
        if source == "whatsapp":
            prompt = INTERPRET_RESULT_WHATSAPP_PROMPT.format(notebook=notebook_filtered, question=question)

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
    