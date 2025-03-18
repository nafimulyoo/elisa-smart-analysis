import requests
from metagpt.tools.tool_registry import register_tool

@register_tool()
def fetch_compare(date: str):
    """
    Fetch energy and cost comparison data for all faculties for a specific month.

    Args:
        date (str): The month and year in 'YYYY-MM' format.

    Returns:
        dict: A dictionary containing the following keys:
            - "value": A list of dictionaries, each containing:
                - "fakultas": The faculty name.
                - "energy": The energy consumption for the faculty.
                - "cost": The cost associated with the energy consumption.
            - "data": A dictionary containing:
                - "max": The faculty with the maximum energy consumption and cost.
                - "min": The faculty with the minimum energy consumption and cost.
                - "total": The total energy consumption and cost across all faculties.
                - "average": The average energy consumption and cost across all faculties.
            - "info": A list of dictionaries, each containing detailed information about a faculty:
                - "faculty": The faculty name.
                - "energy": The energy consumption.
                - "cost": The cost associated with the energy consumption.
                - "area": The area of the faculty.
                - "ike": The energy efficiency index.
                - "students": The number of students.
                - "specific energy": The specific energy consumption per student.
    """
    url = f"https://elisa.itb.ac.id/api/compare?date={date}"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

@register_tool()
def fetch_heatmap(start: str, end: str, faculty: str = "", building: str = "", floor: str = ""):
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
            - "heatmap": A list of dictionaries, each containing:
                - "day": The day of the week (1 = Monday, 7 = Sunday).
                - "hour": The hour of the day (0 = midnight, 23 = 11 PM).
                - "value": The energy consumption value for the given day and hour.
    """
    url = f"https://elisa.itb.ac.id/api/heatmap?faculty={faculty}&start={start}&end={end}&building={building}&floor={floor}"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

@register_tool()
def fetch_monthly(date: str, faculty: str = "", building: str = "", floor: str = ""):
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
                - "timestamp": The timestamp for the data point.
                - "R": Energy consumption for phase R.
                - "S": Energy consumption for phase S.
                - "T": Energy consumption for phase T.
            - "daily_data": A list of dictionaries, each containing:
                - "timestamp": The timestamp for the data point.
                - "cost": The cost for the day.
                - "energy": The energy consumption for the day.
                - "phase 1": Energy consumption for phase 1.
                - "phase 2": Energy consumption for phase 2.
                - "phase 3": Energy consumption for phase 3.
            - "month_data": A dictionary containing:
                - "total_daya": Total energy consumption for the month.
                - "avg_daya": Average energy consumption per day.
                - "total_cost": Total cost for the month.
                - "avg_cost": Average cost per day.
            - "prev_month_data": A dictionary containing the same keys as "month_data" for the previous month.
    """
    url = f"https://elisa.itb.ac.id/api/monthly?date={date}&faculty={faculty}&building={building}&floor={floor}"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

@register_tool()
def fetch_daily(date: str, faculty: str = "", building: str = "", floor: str = ""):
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
                - "timestamp": The timestamp for the data point.
                - "R": Energy consumption for phase R.
                - "S": Energy consumption for phase S.
                - "T": Energy consumption for phase T.
            - "hourly_data": A list of dictionaries, each containing:
                - "hour": The hour of the day (e.g., "01:00").
                - "cost": The cost for the hour.
                - "energy": The energy consumption for the hour.
            - "today_data": A dictionary containing:
                - "total_daya": Total energy consumption for the day.
                - "avg_daya": Average energy consumption per hour.
                - "total_cost": Total cost for the day.
                - "avg_cost": Average cost per hour.
            - "prev_month_data": A dictionary containing the same keys as "today_data" for the previous month.
    """
    url = f"https://elisa.itb.ac.id/api/daily?date={date}&faculty={faculty}&building={building}&floor={floor}"
    print(url)
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

@register_tool()
def fetch_now(date: str):
    """
    Fetch real-time energy data for the current timestamp.

    Args:
        date (str): The date in 'YYYY-MM-DD' format.
        faculty (str, optional): Filter by faculty code (e.g., 'FTI').
        building (str, optional): Filter by building code (e.g., 'LABTEK IV').
        floor (str, optional): Filter by floor code (e.g., 'LANTAI 1').
    Example:
        fetch_now("2023-03-01", faculty="FTI", building="LABTEK IV", floor="LANT
    Returns:
        dict: A dictionary containing the following keys:
            - "chart_data": A list of dictionaries, each containing:
                - "timestamp": The timestamp for the data point.
                - "power": The power consumption at the given timestamp.
            - "today_data": A dictionary containing:
                - "total_daya": Total energy consumption for the day.
                - "avg_daya": Average energy consumption.
                - "total_cost": Total cost for the day.
                - "avg_cost": Average cost.
            - "prev_month_data": A dictionary containing the same keys as "today_data" for the previous month.
    """
    url = f"https://elisa.itb.ac.id/api/now?date={date}&faculty={faculty}&building={building}&floor={floor}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

@register_tool()
def fetch_fakultas():
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
def fetch_gedung(fakultas: str):
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
def fetch_lantai(fakultas: str, gedung: str):
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