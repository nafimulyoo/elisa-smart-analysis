from fastapi import HTTPException
from actions.respond_initial_prompt import RespondInitialPrompt

class InitialPromptHandler:
    def __init__(self, context):
        self.context = context
        self.respond_initial_prompt = RespondInitialPrompt()
        self.max_retry = 3

    async def run(self, prompt):
        result = await self.respond_initial_prompt.run(prompt)

        while self.max_retry > 0:
            if result.type not in ["Basic Analysis", "Advanced Analysis", "Final Answer"]:
                result = await self.respond_initial_prompt.run(prompt)
                self.max_retry -= 1
            else:
                break
        
        if result.type not in ["Basic Analysis", "Advanced Analysis", "Final Answer"]:
            raise HTTPException(status_code=400, detail="Prompt validation failed")
        
        return result
    
    
    