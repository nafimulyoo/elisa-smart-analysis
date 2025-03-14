from api_model import InitialPromptHandlerResult
from fastapi import HTTPException

class RespondInitialPrompt():
    name: str = "RespondInitialPrompt"

    async def run(self, prompt):
        
        if prompt == "irrelevant":
            return InitialPromptHandlerResult(
                type="Final Answer",
                message="Prompt tidak relevan dengan use case ELISA."
            )
        
        if prompt == "no data":
            return InitialPromptHandlerResult(
                type="Final Answer",
                message="Tidak ada data yang bisa diolah."
            )

        if prompt == "general":
            return InitialPromptHandlerResult(
                type="Final Answer",
                message="ELISA adalah singkatan dari Sistem Informasi Energi Listrik dan Air."
            )

        if prompt == "basic":
            return InitialPromptHandlerResult(
                type="Basic Analysis",
                message="Prompt valid dan relevan dengan use case ELISA."
            )
        
        if prompt == "advanced":
            return InitialPromptHandlerResult(
                type="Advanced Analysis",
                message="Prompt valid dan relevan dengan use case ELISA."
            )
        
        else:
            raise HTTPException(status_code=400, detail="Prompt tidak dikenali.")