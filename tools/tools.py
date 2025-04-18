import requests
from metagpt.tools.tool_registry import register_tool

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


import requests
from metagpt.tools.tool_registry import register_tool
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from metagpt.tools.tool_registry import register_tool
import matplotlib.pyplot as plt
import pandas as pd
from prophet import Prophet
from metagpt.tools.tool_registry import register_tool



fetch_elisa_api_data = ["async_fetch_compare", "async_fetch_heatmap", "async_fetch_monthly", "async_fetch_daily", "async_fetch_now", "async_fetch_fakultas", "async_fetch_gedung", "async_fetch_lantai"]


@register_tool()
async def async_fetch_now(faculty: str = "", building: str = "", floor: str = ""):
    """
    Fetch real-time energy data for the last hour and today summary.

    Args:
        faculty (str, optional): Filter by faculty code (e.g., 'FTI').
        building (str, optional): Filter by building code (e.g., 'LABTEK IV').
        floor (str, optional): Filter by floor code (e.g., 'LANTAI 1').
    Example:
        fetch_now(faculty="FTI", building="LABTEK IV", floor="LANTAI 1")
    Returns:
        dict: A dictionary containing the following keys:
            - "chart_data": A list of dictionaries, each containing:
                - "timestamp": The timestamp for the data point in 'YYYY-MM-DD HH:MM:SS' format.
                - "power": The power consumption at the given timestamp. (kW)
            - "today_data": A dictionary containing:
                - "total_daya": Total energy consumption for the day. (kWh)
                - "avg_daya": Average energy consumption per hour. (kWh/hour)
                - "total_cost": Total cost for the day. (Rupiah)
                - "avg_cost": Average cost per hour. (Rupiah/hour)
            - "prev_month_data": A dictionary containing:
                - "total_daya": Total energy consumption for the previous month. (kWh)
                - "total_cost": Total cost for the previous month. (Rupiah)
                - "day_daya": Daily energy consumption for the previous month. (kWh/day)
                - "day_cost": Daily cost for the previous month. (Rupiah/day)
                - "hour_daya": Hourly energy consumption for the previous month. (kWh/hour)
                - "hour_cost": Hourly cost for the previous month. (Rupiah/hour)
    """
    url = f"https://elisa.itb.ac.id/api/now?faculty={faculty}&building={building}&floor={floor}"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")
 
@register_tool()
async def async_fetch_daily(date: str, faculty: str = "", building: str = "", floor: str = ""):
    """
    Fetch daily energy and cost data for a specific date.

    Args:
        date (str): The date in 'YYYY-MM-DD' format.
        faculty (str, optional): Filter by faculty code (e.g., 'FTI').
        building (str, optional): Filter by building code (e.g., 'LABTEK IV').
        floor (str, optional): Filter by floor code (e.g., 'LANTAI 1').
    Example:
        fetch_daily("2023-03-01", faculty="FTI", building="LABTEK IV", floor="LANTAI 1")
    Returns:
        dict: A dictionary containing the following keys:
            - "chart_data": A list of dictionaries, each containing:
                - "timestamp": The timestamp for the data point in 'YYYY-MM-DD HH:MM:SS' format.
                - "R": Energy consumption for phase R. (kWh) 
                - "S": Energy consumption for phase S. (kWh)
                - "T": Energy consumption for phase T. (kWh)
            - "hourly_data": A list of dictionaries, each containing:
                - "hour": The hour of the day in 'HH:00' format, measured per one hour.
                - "cost": The cost for the hour. (Rupiah)
                - "energy": The energy consumption for the hour. (kWh)
            - "today_data": A dictionary containing:
                - "total_daya": Total energy consumption for the day. (kWh)
                - "avg_daya": Average energy consumption per hour. (kWh/hour)
                - "total_cost": Total cost for the day. (Rupiah)
                - "avg_cost": Average cost per hour. (Rupiah/hour)
            - "prev_month_data": A dictionary containing:
                - "total_daya": Total energy consumption for the month. (kWh)
                - "day_daya": Average energy consumption per day. (kWh/day)
                - "total_cost": Total cost for the month. (Rupiah)
                - "day_cost": Average cost per day. (Rupiah/day)
    """
    url = f"https://elisa.itb.ac.id/api/daily?date={date}&faculty={faculty}&building={building}&floor={floor}"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

@register_tool()
async def async_fetch_monthly(date: str, faculty: str = "", building: str = "", floor: str = ""):
    """
    Fetch monthly energy and cost data for a specific month.

    Args:
        date (str): The month and year in 'YYYY-MM' format.
        faculty (str, optional): Filter by faculty code (e.g., 'FTI').
        building (str, optional): Filter by building code (e.g., 'LABTEK IV').
        floor (str, optional): Filter by floor code (e.g., 'LANTAI 1').

    Returns:
        dict: A dictionary containing the following keys:
            - "chart_data": A list of dictionaries, each containing:
                - "timestamp": The timestamp for the data point in 'YYYY-MM-DD HH:MM:SS' format.
                - "R": Energy consumption for phase R. (kWh) 
                - "S": Energy consumption for phase S. (kWh)
                - "T": Energy consumption for phase T. (kWh)
            - "daily_data": A list of dictionaries, each containing:
                - "timestamp": The timestamp for the data point in 'YYYY-MM-DD HH:MM:SS' format.
                - "cost": The cost for the day. (Rupiah)
                - "energy": The energy consumption for the day. (kWh)
                - "phase 1": Energy consumption for phase 1 (R). (kWh)
                - "phase 2": Energy consumption for phase 2 (S). (kWh)
                - "phase 3": Energy consumption for phase 3 (T). (kWh)
            - "month_data": A dictionary containing:
                - "total_daya": Total energy consumption for the month. (kWh)
                - "avg_daya": Average energy consumption per day. (kWh/day)
                - "total_cost": Total cost for the month. (Rupiah)
                - "avg_cost": Average cost per day. (Rupiah/day)
            - "prev_month_data": A dictionary containing:
                - "total_daya": Total energy consumption for the month. (kWh)
                - "day_daya": Average energy consumption per day. (kWh/day)
                - "total_cost": Total cost for the month. (Rupiah)
                - "day_cost": Average cost per day. (Rupiah/day)
    """
    url = f"https://elisa.itb.ac.id/api/monthly?date={date}&faculty={faculty}&building={building}&floor={floor}"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")


@register_tool()
async def async_fetch_heatmap(start: str, end: str, faculty: str = "", building: str = "", floor: str = ""):
    """
    Fetch heatmap data for energy usage over a specified date range.

    Args:
        faculty (str, optional): Filter by faculty code (e.g., 'FTI').
        building (str, optional): Filter by building code (e.g., 'LABTEK IV').
        floor (str, optional): Filter by floor code (e.g., 'LANTAI 1').
        start (str): Start date in 'YYYY-MM-DD' format.
        end (str): End date in 'YYYY-MM-DD' format.

    Returns:
        dict: A dictionary containing the following keys:
            - "dates": A dictionary with "start" and "end" dates.
                - "start": Date when the data collection started in 'YYYY-MM-DD' format.
                - "end": Date when the data collection ended in 'YYYY-MM-DD' format.
            - "heatmap": A list of dictionaries, each containing:
                - "day": The day of the week (1 = Sunday, 2 = Monday, ..., 7 = Saturday).
                - "hour": The hour of the day (0 = midnight, 23 = 11 PM).
                - "value": The energy consumption value for the given day and hour. (kWh)
    """
    url = f"https://elisa.itb.ac.id/api/heatmap?faculty={faculty}&start={start}&end={end}&building={building}&floor={floor}"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

@register_tool()
async def async_fetch_compare(date: str):
    """
    Fetch energy and cost comparison data for all faculties for a specific month. Can also be used to get summary monthly data (total cost and energy) of each faculty efficiently

    Args:
        date (str): The month and year in 'YYYY-MM' format.

    Returns:
        dict: A dictionary containing the following keys:
            - "value": A list of dictionaries, each containing:
                - "fakultas": The faculty name. (FTI, FSRD, etc.)
                - "energy": The energy consumption for the faculty in the month. (kWh)
                - "cost": The cost associated with the energy consumption in the month. (Rupiah)
            - "data": A dictionary containing:
                - "max": A dictionary with the faculty with the maximum energy consumption and cost in the month.
                    - "fakultas": The faculty name. (FTI, FSRD, etc.)
                    - "energy": The maximum energy consumption in the month. (kWh)
                    - "cost": The maximum cost associated with the energy consumption in the month. (Rupiah)
                - "min": A dictionary with the faculty with the minimum energy consumption and cost in the month.
                    - "fakultas": The faculty name. (FTI, FSRD, etc.)
                    - "energy": The minimum energy consumption in the month. (kWh)
                    - "cost": The minimum cost associated with the energy consumption in the month. (Rupiah)
                - "total": A dictionary with the total energy consumption and cost across all faculties in the month.
                    - "total": The total energy consumption in the month. (kWh)
                    - "cost": The total cost associated with the energy consumption in the month. (Rupiah)
                - "average": A dictionary he average energy consumption and cost across all faculties in the month.
                    - "average": The average energy consumption in the month. (kWh)
                    - "cost": The average cost associated with the energy consumption in the month. (Rupiah)
            - "info": A list of dictionaries, each containing detailed information about a faculty:
                - "faculty": The faculty name. (FTI, FSRD, etc.)
                - "energy": The energy consumption in the month. (kWh)
                - "cost": The cost associated with the energy consumption in the month. (Rupiah)
                - "area": The area of the faculty. (m2)
                - "ike": The energy efficiency index. (kWh/m2)
                - "students": The number of students. 
                - "specific energy": The specific energy consumption per student. (kWh/student)
    """
    url = f"https://elisa.itb.ac.id/api/compare?date={date}"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

@register_tool()
async def async_fetch_fakultas():
    """
    Fetch a list of faculties.
    

    Returns:
        dict: A dictionary containing the following key:
            - "fakultas": A list of dictionaries, each containing:
                - "label": The display name of the faculty.
                - "value": The code for the faculty.
    """
    url = "https://elisa.itb.ac.id/api/get-fakultas"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

@register_tool()
async def async_fetch_gedung(fakultas: str):
    """
    Fetch a list of buildings for a specific faculty.

    Args:
        fakultas (str): The faculty code (e.g., 'FTI').

    Returns:
        dict: A dictionary containing the following key:
            - "gedung": A list of dictionaries, each containing:
                - "value": The code for the building.
                - "label": The display name of the building.
    """
    url = f"https://elisa.itb.ac.id/api/get-gedung?fakultas={fakultas}"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

@register_tool()
async def async_fetch_lantai(fakultas: str, gedung: str):
    """
    Fetch a list of floors for a specific building.

    Args:
        fakultas (str): The faculty code (e.g., 'FTI').
        gedung (str): The building code (e.g., 'LABTEK IV').

    Returns:
        dict: A dictionary containing the following key:
            - "lantai": A list of dictionaries, each containing:
                - "label": The display name of the floor.
                - "value": The code for the floor.
    """
    url = f"https://elisa.itb.ac.id/api/get-lantai?fakultas={fakultas}&gedung={gedung}"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    


import requests
from metagpt.tools.tool_registry import register_tool
import pandas as pd
from datetime import datetime

@register_tool()
def save_csv(dataframe: pd.DataFrame, title: str):
    """
    Save the given DataFrame to a CSV file. This is important to ensure that the data is saved and can be accessed later.

    Args:
        data (pd.DataFrame): The DataFrame to save.
        title (str): The title to use for the saved CSV file.

    Returns:
        str: The path to the saved CSV file.
    """
    record_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    data_dir = f"data/output/csv/analysis_data_{record_time}_{title}.csv"
    dataframe.to_csv(data_dir, index=False)
    print(f"Data saved to {data_dir}")
    return data_dir

@register_tool()
def save_plot_image(plt, title: str) :
    """
    Save the given plot to an image file. This is important to ensure that the plot is saved and can be accessed later.

    Args:
        plt: The plot to save.
        title (str): The title to use for the saved image file.

    Returns:
        str: The path to the saved image file.
    """
    record_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_dir = f"data/output/images/plot_{record_time}_{title}.png"
    plt.savefig(image_dir)
    print(f"Image saved to {image_dir}")
    return image_dir

@register_tool()
def kmeans_clustering_auto(dataframe: pd.DataFrame, max_clusters: int = 10, random_state: int = 42) -> pd.DataFrame:
    """
    Perform KMeans clustering on the input DataFrame with automatic determination of the optimal number of clusters.

    Args:
        dataframe (pd.DataFrame): The input DataFrame containing numerical data for clustering.
        max_clusters (int): The maximum number of clusters to consider. Default is 10.
        random_state (int): Random seed for reproducibility. Default is 42.

    Returns:
        pd.DataFrame: The input DataFrame with an additional column 'cluster' for cluster labels.
    """
    # Select only numerical columns for clustering
    X = dataframe.select_dtypes(include=['number'])

    # Calculate Within-Cluster-Sum of Squared Errors (WCSS) for different numbers of clusters
    wcss = []
    silhouette_scores = []
    cluster_range = range(2, max_clusters + 1)

    for n in cluster_range:
        kmeans = KMeans(n_clusters=n, random_state=random_state)
        kmeans.fit(X)
        wcss.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(X, kmeans.labels_))

    # Determine the optimal number of clusters using the Elbow Method
    optimal_clusters = _find_optimal_clusters(wcss, cluster_range)

    # Perform KMeans clustering with the optimal number of clusters
    kmeans = KMeans(n_clusters=optimal_clusters, random_state=random_state)
    clusters = kmeans.fit_predict(X)

    # Add cluster labels to the DataFrame
    dataframe['cluster'] = clusters

    return dataframe

def _find_optimal_clusters(wcss: list, cluster_range: range) -> int:
    """
    Determine the optimal number of clusters using the Elbow Method.

    Args:
        wcss (list): List of Within-Cluster-Sum of Squared Errors (WCSS) for each number of clusters.
        cluster_range (range): Range of cluster numbers considered.

    Returns:
        int: The optimal number of clusters.
    """
    # Calculate the differences in WCSS
    wcss_diff = np.diff(wcss)
    wcss_diff_ratio = wcss_diff[:-1] / wcss_diff[1:]

    # Find the "elbow" point (where the change in WCSS starts to level off)
    optimal_clusters = cluster_range[np.argmax(wcss_diff_ratio) + 1]
    return optimal_clusters


@register_tool()
def prophet_forecast(dataframe: pd.DataFrame, timestamp_col: str, y_cols: list, periods: int = 30) -> pd.DataFrame:
    """
    Perform time series forecasting using Prophet for multiple y columns independently.

    Args:
        dataframe (pd.DataFrame): The input DataFrame containing the timestamp and y columns.
        timestamp_col (str): The name of the timestamp column.
        y_cols (list): A list of column names to predict.
        periods (int): The number of future periods to forecast. Default is 30.

    Returns:
        pd.DataFrame: A DataFrame containing the forecasted values for all y columns.
    """
    results = []

    for y_col in y_cols:
        # Prepare data for Prophet
        df = dataframe[[timestamp_col, y_col]].rename(columns={timestamp_col: 'ds', y_col: 'y'})

        # Initialize and fit Prophet model
        model = Prophet()
        model.fit(df)

        # Make future dataframe and predict
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)

        # Add y_col name to the forecast columns
        forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
        forecast.columns = ['ds', f'{y_col}_yhat', f'{y_col}_yhat_lower', f'{y_col}_yhat_upper']

        # Append to results
        results.append(forecast)

    # Merge all forecasts on the 'ds' column
    final_forecast = results[0]
    for result in results[1:]:
        final_forecast = final_forecast.merge(result, on='ds', how='outer')

    return final_forecast