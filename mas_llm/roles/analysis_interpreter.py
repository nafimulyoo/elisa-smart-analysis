from api_model import InitialPromptHandlerResult

from fastapi import HTTPException
from mas_llm.actions.interpret_result import InterpretResult


from metagpt.logs import logger
from metagpt.roles.role import Role

from metagpt.schema import Message

class AnalysisInterpreter(Role):
    name: str = "Explainer"
    profile: str = "AnalysisInterpreter"

    def __init__(self, source, **kwargs):
        super().__init__(**kwargs)
        self.source = source
        self.interpret_result = InterpretResult()

    async def _act(self):
        logger.info(f"🟢 AnalysisInterpreter: Interpreting analysis")
        msg = self.get_memories(k=1)[0]

        todo = self.rc.todo

        logger.info(f"⚠️ AnalysisInterpreter: Interpreting...")
        result = await self.interpret_result.run(msg.content, self.source)

        msg = Message(content=result, role=self.profile, cause_by=type(todo))

        self.rc.memory.add(msg)
        return msg.content
    