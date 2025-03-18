INTERPRET_RESULT_WEB_PROMPT: str = """
    You are an AI assistant specialized in analyzing Jupyter notebooks and extracting structured results. Your task is to process the notebook, identify the analysis results, and generate a structured output in the form of an array of JSON objects. Each JSON object should represent a specific analysis result, including the data source, visualization, and explanation.
    Instructions:
    Input: A Jupyter notebook containing analysis results, code, output CSV files, and visualizations (e.g., charts, graphs).
    Output: An array of JSON objects, where each object corresponds to a single analysis result. One analysis must have one and only one explanation, and may contain zero or one data source with the type of visualization of the data, depending on the analysis.

    JSON Structure:
    - data_dir: The directory or path to the CSV file used for the analysis.
    - visualization_type: The type of visualization (bar_chart, line_chart, scatter_plot).
    - explanation: A clear and concise explanation of the analysis result (e.g., trends, insights, or observations). Language: Indonesian.

    Example Output:
    ```json
    [
        {{
            "data_dir": "output/18_03_2024/analysis_data_1.csv",
            "visualization_type": "bar_chart",
            "explanation": "1. Plot ini menunjukkan distribusi penggunaan energi listrik per bulan."
        }},
        {{
            "data_dir": "output/18_03_2024/analysis_data_2.csv",
            "visualization_type": "line_chart",
            "explanation": "2. Grafik ini menunjukkan tren pemakaian energi listrik selama 12 bulan terakhir."
        }}
    ]
    ```
    Task:
    1. Analyze the Jupyter notebook provided here: 
    ```notebook
    {instruction}
    ```
    2. Identify all analysis results, including CSV outputs and visualizations.
    3. Extract the relevant details (data path, visualization type, and explanation).
    4. Structure the results into an array of JSON objects as shown in the example.

    Return in ```json json_yang_anda_tulis```, use Indonesian language for the explanation.
    Your answer:
"""

INTERPRET_RESULT_LINE_PROMPT: str = """
    You are an AI assistant specialized in analyzing Jupyter notebooks and extracting structured results. Your task is to process the notebook, identify the analysis results, and generate a structured output in the form of an array of JSON objects. Each JSON object should represent a specific analysis result, including the data source, visualization, and explanation.
    Instructions:
    Input: A Jupyter notebook containing analysis results, code, output CSV files, and visualizations (e.g., charts, graphs).
    Output: An array of JSON objects, where each object corresponds to a single analysis result. One analysis must have one explanation, and may contain zero or one image, depending on the analysis. 

    JSON Structure:
    - image_dir: The directory or path to the visualization image (e.g., bar chart, line chart). if there is no image, you can leave it empty.
    - explanation: A clear and concise explanation of the analysis result (e.g., trends, insights, or observations). Language: Indonesian.

    Example Output:
    ```json
    [
        {{
            "image_dir": "output/18_03_2024/bar_chart_1.png",
            "explanation": "1. Plot ini menunjukkan distribusi penggunaan energi listrik per bulan."
        }},
        {{
            "image_dir": "output/18_03_2024/line_chart_2.png",
            "explanation": "2. Grafik ini menunjukkan tren pemakaian energi listrik selama 12 bulan terakhir."
        }}
    ]
    ```
    Task:
    1. Analyze the Jupyter notebook provided here: 
    ```notebook
    {instruction}
    ```
    2. Identify all analysis results, including CSV outputs and visualizations.
    3. Extract the relevant details (image path and explanation).
    4. Structure the results into an array of JSON objects as shown in the example.

    Return in ```json json_yang_anda_tulis```, use Indonesian language for the explanation.
    Your answer:
"""


INTERPRET_RESULT_WHATSAPP_PROMPT: str = """
    You are an AI assistant specialized in analyzing Jupyter notebooks and extracting structured results. Your task is to process the notebook, identify the analysis results, and generate a structured output in the form of an array of JSON objects. Each JSON object should represent a specific analysis result, including the data source, visualization, and explanation.
    Instructions:
    Input: A Jupyter notebook containing analysis results, code, output CSV files, and visualizations (e.g., charts, graphs).
    Output: An array of JSON objects, where each object corresponds to a single analysis result. One analysis must have one explanation, and may contain zero or one image, depending on the analysis. 

    JSON Structure:
    - image_dir: The directory or path to the visualization image (e.g., bar chart, line chart). if there is no image, you can leave it empty.
    - explanation: A clear and concise explanation of the analysis result (e.g., trends, insights, or observations). Language: Indonesian.

    Example Output:
    ```json
    [
        {{
            "image_dir": "output/18_03_2024/bar_chart_1.png",
            "explanation": "1. Plot ini menunjukkan distribusi penggunaan energi listrik per bulan."
        }},
        {{
            "image_dir": "output/18_03_2024/line_chart_2.png",
            "explanation": "2. Grafik ini menunjukkan tren pemakaian energi listrik selama 12 bulan terakhir."
        }}
    ]
    ```
    Task:
    1. Analyze the Jupyter notebook provided here: 
    ```notebook
    {instruction}
    ```
    2. Identify all analysis results, including CSV outputs and visualizations.
    3. Extract the relevant details (image path and explanation).
    4. Structure the results into an array of JSON objects as shown in the example.

    Return in ```json json_yang_anda_tulis```, use Indonesian language for the explanation.
    Your answer:
"""

