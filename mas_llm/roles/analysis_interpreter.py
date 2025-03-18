from api_model import InitialPromptHandlerResult

from fastapi import HTTPException
from mas_llm.actions.interpret_result import InterpretResult

from metagpt.logs import logger
from metagpt.roles.role import Role


class AnalysisInterpreter(Role):
    name: str = "Explainer"
    profile: str = "AnalysisInterpreter"
    source: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.interpret_result = InterpretResult()

    def set_source(self, source):
        self.source = source

    async def _act(self):
        logger.info(f"🟢 AnalysisInterpreter: Interpreting analysis")
        msg = self.get_memories(k=1)[0]

        logger.info(f"⚠️ AnalysisInterpreter: Interpreting...")
        result = await self.interpret_result.run(instruction=msg.content, source=self.source)

        return result
    

    