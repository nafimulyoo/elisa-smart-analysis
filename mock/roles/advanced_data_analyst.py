from fastapi import HTTPException
from mock.actions.write_analysis_code import WriteAnalysisCode
from mock.actions.review_code import ReviewCode
from mock.actions.execute_code import ExecuteCode
from mock.actions.solution_planner import SolutionPlanner


class AdvancedDataAnalyst:
    def __init__(self, context):
        self.context = context
        self.write_analysis_code = WriteAnalysisCode()
        self.execute_code = ExecuteCode()
        self.review_code = ReviewCode()
        self.solution_planner = SolutionPlanner()
        self.max_retry = 3

    async def run(self, prompt):
        plan = await self.solution_planner.run(prompt)

        for step in plan:
            code_text = self.write_analysis_code.run(prompt, review=None)
            code_execution_result = self.execute_code.run(code_text)
            
            while self.max_retry > 0:
                if "error" in code_execution_result:
                    code_review = self.review_code.run(code_text)
                    code_text = self.write_analysis_code.run(prompt, code_review)
                    code_execution_result = self.execute_code.run(code_text)
                    self.max_retry -= 1
                else:
                    break

            if "error" in code_execution_result:
                raise HTTPException(status_code=400, detail="Code execution failed")
        
        return code_execution_result

        
    

    