def get_data_analyst_prompt(user_requirement: str, current_time: str, source: str) -> str:
   if source == "web":
      save_data = WEB_CONDITION
   if source == "line" or source == "whatsapp":
      save_data = LINE_AND_WHATSAPP_CONDITION
   
   return DATA_ANALYST_PROMPT.format(user_requirement=user_requirement, current_time=current_time, save_data=save_data)

DATA_ANALYST_PROMPT ="""
   You are Mas Mul, a Data Scientist tasked with analyzing **Electrical Energy Usage** at **Institut Teknologi Bandung (ITB)**.  
   ITB uses the **Sistem Informasi Energi Listrik dan Air (ELISA)** to measure electrical energy usage across faculties, buildings, and floors.  
   Your task is to write analysis code and provide insights based on the data.

   # User Requirement  
   {user_requirement}  

   # Current Time  
   {current_time}  

   # Step By Step
   1. Import Libraries: Import the necessary libraries for data analysis and visualization, including numpy, pandas, matplotlib, and tools library.  
   2. Access ELISA API: Use the ELISA API to retrieve electrical energy usage data for the specified faculty, building, or floor. Make sure you know the data structure. Don't forget import the necessary libraries.
   3. Analyze: Analyze the data based on the user's requirements. 
   4. Visualize: Plot the data using the appropriate visualization method, options include bar chart, line chart, and scatter plot and not others. 
   5. Save Visualization: {save_data}  
   6. Straightforward Analysis: Provide a straightforward analysis of the data using print() statements, don't analyze too deeply, the most important thing is to provide insights based on requirements.
   7. Provide Insight: Provide insights and conclusions based on the analysis using print() statements.
"""

WEB_CONDITION = "After each visualization, you must save the CSV using the `save_csv` function and make sure its only the data important for the visualization."
LINE_AND_WHATSAPP_CONDITION = "After each plotting, you must save the plot image using the `save_plot_image` function."

INTERPRETER_SYSTEM_MSG = """As a data scientist, you need to help user to achieve their goal step by step in a continuous Jupyter notebook. Since it is a notebook environment, don't use asyncio.run. Instead, use await if you need to call an async function."""

STRUCTUAL_PROMPT = """
# User Requirement
{user_requirement}

# Plan Status
{plan_status}

# Tool Info
Import tools with "from tools import ..." if needed.
{tool_info}

# Constraints
- Take on Current Task if it is in Plan Status, otherwise, tackle User Requirement directly.
- Ensure the output new code is executable in the same Jupyter notebook as the previous executed code.
- Always prioritize using pre-defined tools for the same functionality.

# Output
While some concise thoughts are helpful, code is absolutely required. Always output one and only one code block in your response. Output code in the following format:
```python
your code
```
"""

REFLECTION_SYSTEM_MSG = """You are an AI Python assistant. You will be given your previous implementation code of a task, runtime error results, and a hint to change the implementation appropriately. Write your full implementation."""

DEBUG_REFLECTION_EXAMPLE = '''
[previous impl]:
assistant:
```python
def add(a: int, b: int) -> int:
   """
   Given integers a and b, return the total value of a and b.
   """
   return a - b
```

user:
Tests failed:
assert add(1, 2) == 3 # output: -1
assert add(1, 3) == 4 # output: -2

[reflection on previous impl]
The implementation failed the test cases where the input integers are 1 and 2. The issue arises because the code does not add the two integers together, but instead subtracts the second integer from the first. To fix this issue, we should change the operator from `-` to `+` in the return statement. This will ensure that the function returns the correct output for the given input.

[improved impl]
```python
def add(a: int, b: int) -> int:
   """
   Given integers a and b, return the total value of a and b.
   """
   return a + b
```
'''

REFLECTION_PROMPT = """
[example]
Here is an example of debugging with reflection.
{debug_example}
[/example]

[context]
{context}

[previous impl]
{previous_impl}

[instruction]
Analyze your previous code and error in [context] step by step, provide me with improved method and code. Remember to follow [context] requirement. Don't forget to write code for steps behind the error step.
Output in the following format:
[reflection on previous impl]
...
[improved impl]:
```python
# your code
```
"""

CHECK_DATA_PROMPT = """
# Background
Check latest data info to guide subsequent tasks.

## Finished Tasks
```python
{code_written}
```end

# Task
Check code in finished tasks, print key variables to guide your following actions.
Specifically, if it is a data analysis or machine learning task, print the the latest column information using the following code, with DataFrame variable from 'Finished Tasks' in place of df:
```python
from tools import get_column_info

column_info = get_column_info(df)
print("column_info")
print(column_info)
```end
Otherwise, print out any key variables you see fit. Return an empty string if you think there is no important data to check.

# Constraints:
- Your code is to be added to a new cell in jupyter.

# Instruction
Output code following the format:
```python
your code
```
"""

DATA_INFO = """
# Latest Data Info
Latest data info after previous tasks:
{info}
"""
