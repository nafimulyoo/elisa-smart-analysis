from api_model import InitialPromptHandlerResult
from fastapi import HTTPException

class RespondInitialPrompt():
    name: str = "RespondInitialPrompt"

    async def run(self, prompt):
        # LOGIC HERE
        
        if prompt == "irrelevant":
            return InitialPromptHandlerResult(
                type="Final Answer",
                message="Prompt tidak relevan dengan use case ELISA."
            )
        
        elif prompt == "no data":
            return InitialPromptHandlerResult(
                type="Final Answer",
                message="Tidak ada data yang bisa diolah."
            )

        elif prompt == "general":
            return InitialPromptHandlerResult(
                type="Final Answer",
                message="ELISA adalah singkatan dari Sistem Informasi Energi Listrik dan Air."
            )

        elif prompt == "basic":
            return InitialPromptHandlerResult(
                type="Basic Analysis",
                message="Prompt valid dan relevan dengan use case ELISA."
            )
        
        elif prompt == "advanced":
            return InitialPromptHandlerResult(
                type="Advanced Analysis",
                message="Prompt valid dan relevan dengan use case ELISA."
            )
        
        else:
            return InitialPromptHandlerResult(
                type="Fail",
                message="Prompt tidak valid."
            )