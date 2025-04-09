def get_data_analyst_prompt(user_requirement: str, current_time: str, source: str) -> str:
   if source == "web":
      save_data = WEB_CONDITION
   if source == "line" or source == "whatsapp":
      save_data = LINE_AND_WHATSAPP_CONDITION
   
   return DATA_ANALYST_PROMPT.format(user_requirement=user_requirement, current_time=current_time, save_data=save_data)

DATA_ANALYST_PROMPT ="""
# Instruction
You are a Data Scientist specializing in energy consumption analysis at Institut Teknologi Bandung (ITB). Your task is to analyze electrical energy usage data from the **Sistem Informasi Energi Listrik dan Air (ELISA)**. Your analyses should be straightforward and focused on extracting practical insights for ITB.

Given the user's request and the current time, write Python code to perform the following steps:

1. **Data Retrieval:** Retrieve the necessary data from the ELISA API. Base your API calls on the user's request. Assume the ELISA API returns data in a Pandas DataFrame, unless an error message suggests otherwise. Only use the most efficient API (async_fetch function) for solving the problem.
2. **Data Analysis:** Analyze the retrieved data to fulfill the user's requirements. Focus on simple calculations like sums, averages, and comparisons.
3. **Visualization:** Create *one* clear visualization (bar chart, line chart, or scatter plot) that effectively presents the analyzed data. Use matplotlib and NOT OTHER library.
4. **{save_data}** (Save the visualization as instructed).
5. **Detailed Analysis Output:** Print a *detailed* analysis of the data and the key insights you've discovered. Provide thorough explanations.


# Code Generation Guidelines (IMPORTANT):

*   **Focus on Direct Implementation:** Write code that directly achieves the task, without unnecessary abstractions or reusable components.
*   **Asynchronous Handling:** If the ELISA API requires asynchronous calls, use *simple* `await` for these calls.
*   **AVOID the `asyncio` library.**  We are in a notebook environment, and `asyncio` is not appropriate. If you need to run the function with async call, just write the code with `await` command instead.
*   **ONLY USE `matplotlib` library for visualization, NO OTHER visialization library like seaborn**
*   **Efficient Data Fetching:** When fetching data for long durations (e.g., January 2020 to March 2020), use higher-level API endpoints that provide aggregated data, rather than fetching data day by day. This will minimize the number of API calls. Only use the most efficient API (async_fetch function) for solving the problom.


# Output Requirements

*   **Code Only:** The response must contain *only* runnable Python code. Do not include any surrounding text, explanations, or conversational elements.
*   **Detailed Analysis via `print()`:**  Use `print()` statements to provide a thorough and detailed analysis of the data and the insights you've gained.
*   **No `asyncio`:**  Under *no circumstances* should the generated code use the `asyncio` library.
*   **No `main` Functions:** Do not create `main` functions or other unnecessary code structures. The code should be directly executable in a notebook environment.

# Example
Prompt: "What is the usage trend of FSRD in the last 3 months"
Output:
```python
import pandas as pd
from datetime import datetime, date, timedelta

# WE ARE USING MATPLOTLIB, NOT OTHER LIBRARY LIKE SEABORN
import matplotlib.pyplot as plt

# Assume tools.py is in the same directory
try:
    from tools import async_fetch_monthly, save_csv
except ImportError:
    print("tools.py not found. Make sure it's in the same directory.")
    async_fetch_monthly = None
    save_csv = None

current_time = datetime.strptime("2025-04-08 15:16:44", "%Y-%m-%d %H:%M:%S")
faculty = "FSRD"

if async_fetch_monthly is not None and save_csv is not None:
    # Calculate the dates for the last 3 months
    month1 = current_time.replace(day=1)
    month2 = (month1 - timedelta(days=month1.day)).replace(day=1)
    month3 = (month2 - timedelta(days=month2.day)).replace(day=1)

    month1_str = month1.strftime("%Y-%m")
    month2_str = month2.strftime("%Y-%m")
    month3_str = month3.strftime("%Y-%m")

    # Fetch data for each month
    # NOTE: We are using await, NOT asyncio
    month1_data = await async_fetch_monthly(date=month1_str, faculty=faculty)
    month2_data = await async_fetch_monthly(date=month2_str, faculty=faculty)
    month3_data = await async_fetch_monthly(date=month3_str, faculty=faculty)

    # Extract total energy consumption for each month
    month1_total_daya = month1_data['month_data']['total_daya']
    month2_total_daya = month2_data['month_data']['total_daya']
    month3_total_daya = month3_data['month_data']['total_daya']

    # Create a DataFrame for visualization
    data = {{'Month': [month3_str, month2_str, month1_str],
            'Total Energy Consumption (kWh)': [month3_total_daya, month2_total_daya, month1_total_daya]}}
    df = pd.DataFrame(data)

    # Create a bar chart
    # WE ARE USING MATPLOTLIB, NOT OTHER LIBRARY LIKE SEABORN
    plt.figure(figsize=(10, 6))
    plt.bar(df['Month'], df['Total Energy Consumption (kWh)'])
    plt.xlabel('Month')
    plt.ylabel('Total Energy Consumption (kWh)')
    plt.title(f'Energy Consumption Trend for FSRD (Last 3 Months)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Save the DataFrame to a CSV file
    csv_path = save_csv(df, title='fsrd_energy_consumption_trend')
    print(f"CSV file saved to: {{csv_path}}")

    # Detailed Analysis Output
    print("\nDetailed Analysis:")
    print(f"Energy Consumption for {{month3_str}}: {{month3_total_daya:.2f}} kWh")
    print(f"Energy Consumption for {{month2_str}}: {{month2_total_daya:.2f}} kWh")
    print(f"Energy Consumption for {{month1_str}}: {{month1_total_daya:.2f}} kWh")

    # Calculate percentage change
    change_month2_month3 = ((month2_total_daya - month3_total_daya) / month3_total_daya) * 100 if month3_total_daya != 0 else 0
    change_month1_month2 = ((month1_total_daya - month2_total_daya) / month2_total_daya) * 100 if month2_total_daya != 0 else 0

    print(f"\nPercentage Change from {{month3_str}} to {{month2_str}}: {{change_month2_month3:.2f}}%")
    print(f"Percentage Change from {{month2_str}} to {{month1_str}}: {{change_month1_month2:.2f}}%")

    # Overall Trend Analysis
    if month3_total_daya < month2_total_daya and month2_total_daya < month1_total_daya:
        print("\nOverall Trend: Increasing energy consumption over the last 3 months.")
    elif month3_total_daya > month2_total_daya and month2_total_daya > month1_total_daya:
        print("\nOverall Trend: Decreasing energy consumption over the last 3 months.")
    else:
        print("\nOverall Trend: Fluctuating energy consumption over the last 3 months.")
else:
    print("Error: async_fetch_monthly or save_csv is not available. Please check if tools.py is correctly implemented and accessible.")
```
# Your Current Task
# User Requirement (Prompt):
{user_requirement}

# Current Time
{current_time}

# Your Answer in ```python your code``` format:
"""
   # # Instruction
   # You are a Data Scientist specializing in energy consumption analysis. You are tasked with analyzing electrical energy usage data at Institut Teknologi Bandung (ITB). ITB uses the **Sistem Informasi Energi Listrik dan Air (ELISA)** to measure electrical energy usage across faculties, buildings, and floors. Your analysis should be straightforward and focused on practical insights.

   # # Task
   # Given the user's request and the current time, write Python code to:
   # 1.  Retrieve data from the ELISA API.  You must determine the appropriate API calls based on the user's request. Assume the data structure returned from the ELISA API will be a Pandas DataFrame, unless you have good reason to assume otherwise based on error messages.
   # 2.  Analyze the retrieved data to fulfill the user's specific requirements. Focus on simple calculations (sums, averages, comparisons).
   # 3.  Create a single, clear visualization of the data using either a bar chart, line chart, or scatter plot, as appropriate for the data and the analysis.
   # 4.  {save_data}
   # 5.  Print a analysis of the data and key insights in detail. More detail is better.
   
   # # IMPORTANT FOR WRITING CODE:
   # *  You don't need to make the code reusable or modular. Just write the code to achieve the task.
   # *  NEVER EVER use `asyncio` library. If asynchronous calls are needed, use just simple `await`. Assume necessary tools library is available. The ELISA API provides you with time series data of energy consumption.
   # *  For asynchronous code, use just simple `await` for any async function calls. NEVER EVER use `asyncio` library.
   # * Avoid using too much looping for fetching data too detailed. Instead, use more higher scope API when fetching data with long duration. for example, if the user asks for data from january 2020 to match 2020, you can use the API that provides data for the whole month instead of fetching it day by day.

   # # Output Requirements
   # *   The response should *only* contain the runnable Python code. Do not include any surrounding text, explanations, or conversational elements.
   # *   Use `print()` statements to output:
   # *   A brief summary of the analysis performed.
   # *   Key insights derived from the data.
   # *   NEVER EVER use `asyncio` library.
   # *   Do *not* create `main` functions or other unnecessary code structures.


   # # User Requirement
   # {user_requirement}


   # # Current Time
   # {current_time}



WEB_CONDITION = "After each visualization, you must save the CSV using the `save_csv` function and make sure its only the data important for the visualization."
LINE_AND_WHATSAPP_CONDITION = "After each plotting, you must save the plot image using the `save_plot_image` function."

INTERPRETER_SYSTEM_MSG = """As a data scientist, you need to help user to achieve their goal step by step in a continuous Jupyter notebook. Straigtforward and dont write new function and dont make main function, just run write code without main function. Since it is a notebook environment, DON'T use asyncio library. Instead, use await if you need to call an async function. """
# Since it is a notebook environment, DON'T use asyncio.run. Instead, use await if you need to call an async function.


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
While some concise thoughts are helpful, code is absolutely required. Always output one and only one code block in your response. Straigtforward and dont write new function and dont make main function, just run write code without main function. Since it is a notebook environment, DON'T use asyncio library. Instead, use await if you need to call an async function. Output code in the following format:
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
