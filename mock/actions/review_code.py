from api_model import InitialPromptHandlerResult
from fastapi import HTTPException

class ReviewCode:
    name: str = "ReviewCode"

    async def run(self, prompt):
        return "Kode berhasil dieksekeusi."