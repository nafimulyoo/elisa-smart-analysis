from api_model import InitialPromptHandlerResult
from fastapi import HTTPException

class ReviewPrompt():
    name: str = "RespondInitialPrompt"

    async def run(self, prompt):
        return "Kode berhasil dieksekeusi."