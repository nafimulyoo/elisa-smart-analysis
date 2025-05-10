from metagpt.actions import Action
from metagpt.logs import logger
from mas_llm.prompts.page_analysis_prompt import (
    NOW_PROMPT_TEMPLATE,
    DAILY_PROMPT_TEMPLATE,
    MONTHLY_PROMPT_TEMPLATE,
    HEATMAP_PROMPT_TEMPLATE,
    COMPARE_FACULTY_PROMPT_TEMPLATE,
)

from datetime import datetime, timedelta

from functools import wraps
import hashlib
import json
import time
from datetime import datetime
from metagpt.config2 import Config
import os
from pathlib import Path

class AnalyzePage(Action):
    name: str = "AnalyzePage"


deepseek = Config.from_yaml_file(Path("config/deepseek-r1.yaml"))
gemma = Config.from_yaml_file(Path("config/gemma3.yaml"))
gemini = Config.from_yaml_file(Path("config/config2.yaml"))
"""
Analysis objectives:
for now_analysis:
- Analyze the current power consumption data in the context of the past week's energy usage heatmap.
- Highlight any significant deviations from the typical pattern.
- Suggest potential causes for deviations.
- Emphasize actionable insights.
- Compare current data to the trends visible in the heatmap.

for daily_analysis:
- Analyze the daily energy consumption data in the context of the past week's energy usage heatmap.
- Summarize peak usage hours and phase imbalances.
- Compare today's consumption to the patterns in the heatmap.
- Indicate if today's energy use is anomalous, based on what is typical in the heatmap.

for monthly_analysis:
- Analyze the monthly energy consumption data, comparing to recent months.
- Highlight total consumption, peak days, and phase contribution.
- Detect anomalies based on historical data.
- Quantify trends vs historical averages.

for heatmap_analysis:
- Analyze the energy usage heatmap data and identify key patterns.
- Highlight the days of the week and hours of the day with the highest and lowest consumption.
- Detect any significant anomalies.

for compare_faculty_analysis:
- Analyze the energy consumption data for different faculties.
- Identify key differences and rank the faculties by energy consumption.
- Highlight those with significantly higher or lower consumption than the average.
- Compare current faculty consumptions to historical faculty consumptions.
- Point out changes and potential insights.
"""

# Cache storage
analysis_caches = {
    "now": {"data": {}, "timestamps": {}, "order": [], "ttl": 7200},  # 2 hours
    "daily": {"data": {}, "timestamps": {}, "order": [], "ttl": 7200},  # 2 hours
    "monthly": {"data": {}, "timestamps": {}, "order": [], "ttl": 7200},  # 2 hours
    "heatmap": {"data": {}, "timestamps": {}, "order": [], "ttl": 7200},  # 2 hours
    "compare_faculty": {"data": {}, "timestamps": {}, "order": [], "ttl": 7200},  # 2 hours
}

def generate_cache_key(func_name: str, *args, **kwargs) -> str:
    """Generate a consistent cache key for function arguments"""
    # Convert args and kwargs to a consistent string representation
    args_str = json.dumps(args, sort_keys=True)
    kwargs_str = json.dumps(kwargs, sort_keys=True)
    input_str = f"{func_name}-{args_str}-{kwargs_str}"
    
    # Use SHA256 to create a fixed-length key
    return hashlib.sha256(input_str.encode()).hexdigest()

def cached_analysis(func_name: str):
    """Decorator factory for analysis functions with caching"""
    cache_info = analysis_caches[func_name]
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = generate_cache_key(func_name, *args, **kwargs)
            
            # Check cache
            current_time = time.time()
            if cache_key in cache_info["data"]:
                cached_time = cache_info["timestamps"][cache_key]
                if current_time - cached_time < cache_info["ttl"]:
                    # Update access order
                    if cache_key in cache_info["order"]:
                        cache_info["order"].remove(cache_key)
                    cache_info["order"].append(cache_key)
                    return cache_info["data"][cache_key]
            
            # Not in cache or expired - execute function
            result = await func(*args, **kwargs)
            
            # Store in cache
            cache_info["data"][cache_key] = result
            cache_info["timestamps"][cache_key] = current_time
            cache_info["order"].append(cache_key)
            
            # Enforce cache size (100 items)
            if len(cache_info["order"]) > 100:
                oldest_key = cache_info["order"].pop(0)
                del cache_info["data"][oldest_key]
                del cache_info["timestamps"][oldest_key]
            
            return result
        return wrapper
    return decorator

@cached_analysis("now")
async def now_analysis(data, faculty="", building="", floor="", model="") -> str:
    """
    Analyzes last one hour and today energy data, comparing against data last month

    Args:
        data:  A dictionary containing the following keys:
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
    if model == "deepseek":
        analyze_page = AnalyzePage(config=deepseek)
    elif model == "gemma":
        analyze_page = AnalyzePage(config=gemma)
    else:
        analyze_page = AnalyzePage(config=gemini)
    try:
        # Extract Current Data
        
        chart_data = data.get("chart_data", [])
        measurement_start_time = chart_data[0].get("timestamp", "N/A") if chart_data else "N/A"
        measurement_end_time = chart_data[-1].get("timestamp", "N/A") if chart_data else "N/A"

        if not chart_data:
            return "No data available for analysis."


        # peak power value and timestamp
        max_power = max(
            (item.get("power", 0.0) for item in chart_data), default=0.0
        )

        max_timestamp = next(
            (
                item.get("timestamp", "N/A")
                for item in chart_data
                if item.get("power", 0.0) == max_power
            ),
            "N/A",
        )

        min_power = min(
            (item.get("power", 0.0) for item in chart_data), default=0.0
        )

        min_timestamp = next(
            (
                item.get("timestamp", "N/A")
                for item in chart_data
                if item.get("power", 0.0) == min_power
            ),
            "N/A",
        )

        current_power = chart_data[-1].get("power", 0.0) if chart_data else 0.0
        
        total_power_today = data.get("today_data", {}).get("total_daya", 0.0)
        avg_power_per_hour_today = data.get("today_data", {}).get("avg_daya", 0.0)
        total_cost_today = data.get("today_data", {}).get("total_cost", 0.0)
        avg_cost_per_hour_today = data.get("today_data", {}).get("avg_cost", 0.0)

        total_power_prev_month = data.get("prev_month_data", {}).get("total_daya", 0.0)
        total_cost_prev_month = data.get("prev_month_data", {}).get("total_cost", 0.0)
        avg_power_per_day_prev_month = data.get("prev_month_data", {}).get("day_daya", 0.0)
        avg_cost_per_day_prev_month = data.get("prev_month_data", {}).get("day_cost", 0.0)
        avg_power_per_hour_prev_month = data.get("prev_month_data", {}).get("hour_daya", 0.0)
        avg_cost_per_hour_prev_month = data.get("prev_month_data", {}).get("hour_cost", 0.0)

        if faculty == "":
            faculty = "All faculty"
        if building == "":
            building = "All building"
        if floor == "":
            floor = "All floor"

        # get from date
        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        prompt = NOW_PROMPT_TEMPLATE.format(
            current_timestamp=current_timestamp,
            faculty=faculty,
            building=building,
            floor=floor,

            measurement_start_time=measurement_start_time,
            measurement_end_time=measurement_end_time,
            current_power=current_power,

            max_power=max_power,
            max_timestamp=max_timestamp,
            min_power=min_power,
            min_timestamp=min_timestamp,

            total_power_today=total_power_today,
            avg_power_per_hour_today=avg_power_per_hour_today,
            total_cost_today=total_cost_today,
            avg_cost_per_hour_today=avg_cost_per_hour_today,

            total_power_prev_month=total_power_prev_month,
            total_cost_prev_month=total_cost_prev_month,
            avg_power_per_day_prev_month=avg_power_per_day_prev_month,
            avg_cost_per_day_prev_month=avg_cost_per_day_prev_month,
            avg_power_per_hour_prev_month=avg_power_per_hour_prev_month,
            avg_cost_per_hour_prev_month=avg_cost_per_hour_prev_month,
        )

        logger.info(f"↘️ Prompt: {prompt}")
        analysis = await analyze_page._aask(prompt)
        return analysis

    except Exception as e:
        return f"Error generating analysis: {str(e)}"

@cached_analysis("daily")
async def daily_analysis(data, date, faculty="", building="", floor="", model="") -> str:
    """
    Analyzes daily energy data, comparing it to a heatmap of the past week.
    history is the result of async_fetch_heatmap.

    Args:
        data: dict: A dictionary containing the following keys:
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
    if model == "deepseek":
        analyze_page = AnalyzePage(config=deepseek)
    elif model == "gemma":
        analyze_page = AnalyzePage(config=gemma)
    else:
        analyze_page = AnalyzePage(config=gemini)

    try:
        # add Total Power in chart_data R + S + T
        for item in data.get("chart_data", []):
            item["Energy"] = item.get("R", 0) + item.get("S", 0) + item.get("T", 0)

        # Max and Min kWh
        max_energy = max(
            (item.get("Energy", 0.0) for item in data.get("chart_data", [])), default=0.0
        )

        max_timestamp = next(
            (
                item.get("timestamp", "N/A")
                for item in data.get("chart_data", [])
                if item.get("Energy", 0.0) == max_energy
            ),
            "N/A",
        )

        min_energy = min(
            (item.get("Energy", 0.0) for item in data.get("chart_data", [])), default=0.0
        )

        min_timestamp = next(
            (
                item.get("timestamp", "N/A")
                for item in data.get("chart_data", [])
                if item.get("Energy", 0.0) == min_energy
            ),
            "N/A",
        )

        total_energy = data.get("today_data", {}).get("total_daya", 0.0)
        total_cost = data.get("today_data", {}).get("total_cost", 0.0)
        avg_power = data.get("today_data", {}).get("avg_daya", 0.0)
        avg_cost_per_hour = data.get("today_data", {}).get("avg_cost", 0.0)

        total_month_energy_prev_month = data.get("prev_month_data", {}).get("total_daya", 0.0)
        total_month_cost_prev_month = data.get("prev_month_data", {}).get("total_cost", 0.0)
        total_day_energy_prev_month = data.get("prev_month_data", {}).get("day_daya", 0.0)
        total_day_cost_prev_month = data.get("prev_month_data", {}).get("day_cost", 0.0)
        avg_power_prev_month = data.get("prev_month_data", {}).get("day_daya", 0.0)/24.0
        avg_cost_per_hour_prev_month = data.get("prev_month_data", {}).get("day_cost", 0.0)/24.0


        chart_data = data.get("chart_data", [])
        phase_r = (
            sum(item.get("R", 0) for item in chart_data) if chart_data else 0
        )
        phase_s = (
            sum(item.get("S", 0) for item in chart_data) if chart_data else 0
        )
        phase_t = (
            sum(item.get("T", 0) for item in chart_data) if chart_data else 0
        )


        if faculty == "":
            faculty = "All faculty"
        if building == "":
            building = "All building"
        if floor == "":
            floor = "All floor"

        # get from date
        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        prompt = DAILY_PROMPT_TEMPLATE.format(
            current_timestamp=current_timestamp,
            faculty=faculty,
            building=building,
            floor=floor,

            date=date,

            max_energy=max_energy,
            max_timestamp=max_timestamp,
            min_energy=min_energy,
            min_timestamp=min_timestamp,

            total_energy=total_energy,
            total_cost=total_cost,
            avg_power=avg_power,
            avg_cost_per_hour=avg_cost_per_hour,

            phase_r=phase_r,
            phase_s=phase_s,
            phase_t=phase_t,

            total_month_energy_prev_month=total_month_energy_prev_month,
            total_month_cost_prev_month=total_month_cost_prev_month,
            total_day_energy_prev_month=total_day_energy_prev_month,
            total_day_cost_prev_month=total_day_cost_prev_month,
            avg_power_prev_month=avg_power_prev_month,
            avg_cost_per_hour_prev_month=avg_cost_per_hour_prev_month
        )
        logger.info(f"↘️ Prompt: {prompt}")
        analysis = await analyze_page._aask(prompt)
        return analysis
    except Exception as e:
        return f"Error generating analysis: {str(e)}"

@cached_analysis("monthly")
async def monthly_analysis(data, date, faculty="", building="", floor="", model="") -> str:
    """
    Analyzes monthly energy data, comparing to a list of previous months.

    Args:
        data: dict: A dictionary containing the following keys:
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
    if model == "deepseek":
        analyze_page = AnalyzePage(config=deepseek)
    elif model == "gemma":
        analyze_page = AnalyzePage(config=gemma)
    else:
        analyze_page = AnalyzePage(config=gemini)

    try:
        max_energy = max(
            (item.get("energy", 0.0) for item in data.get("daily_data", [])), default=0.0
        )

        max_timestamp = next(
            (
                item.get("timestamp", "N/A")
                for item in data.get("daily_data", [])
                if item.get("energy", 0.0) == max_energy
            ),
            "N/A",
        )

        min_energy = min(
            (item.get("energy", 0.0) for item in data.get("daily_data", [])), default=0.0
        )

        min_timestamp = next(
            (
                item.get("timestamp", "N/A")
                for item in data.get("daily_data", [])
                if item.get("energy", 0.0) == min_energy
            ),
            "N/A",
        )

        total_energy = data.get("month_data", {}).get("total_daya", 0.0)
        total_cost = data.get("month_data", {}).get("total_cost", 0.0)
        avg_power = data.get("month_data", {}).get("avg_daya", 0.0)
        avg_cost_per_day = data.get("month_data", {}).get("avg_cost", 0.0)

        total_month_energy_prev_month = data.get("prev_month_data", {}).get("total_daya", 0.0)
        total_month_cost_prev_month = data.get("prev_month_data", {}).get("total_cost", 0.0)
        total_day_energy_prev_month = data.get("prev_month_data", {}).get("day_daya", 0.0)
        total_day_cost_prev_month = data.get("prev_month_data", {}).get("day_cost", 0.0)


        chart_data = data.get("chart_data", [])
        phase_r = (
            sum(item.get("R", 0) for item in chart_data) if chart_data else 0
        )
        phase_s = (
            sum(item.get("S", 0) for item in chart_data) if chart_data else 0
        )
        phase_t = (
            sum(item.get("T", 0) for item in chart_data) if chart_data else 0
        )


        if faculty == "":
            faculty = "All faculty"
        if building == "":
            building = "All building"
        if floor == "":
            floor = "All floor"


        # get from date
        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        prompt = MONTHLY_PROMPT_TEMPLATE.format(
            current_timestamp=current_timestamp,
            faculty=faculty,
            building=building,
            floor=floor,

            date=date,

            max_energy=max_energy,
            max_timestamp=max_timestamp,
            min_energy=min_energy,
            min_timestamp=min_timestamp,

            total_energy=total_energy,
            total_cost=total_cost,
            avg_power=avg_power,
            avg_cost_per_day=avg_cost_per_day,

            phase_r=phase_r,
            phase_s=phase_s,
            phase_t=phase_t,

            total_month_energy_prev_month=total_month_energy_prev_month,
            total_month_cost_prev_month=total_month_cost_prev_month,
            total_day_energy_prev_month=total_day_energy_prev_month,
            total_day_cost_prev_month=total_day_cost_prev_month,
        )

        logger.info(f"↘️ Prompt: {prompt}")
        analysis = await analyze_page._aask(prompt)
        return analysis
    except Exception as e:
        return f"Error generating analysis: {str(e)}"

@cached_analysis("heatmap")
async def heatmap_analysis(data, history, faculty="", building="", floor="", model="") -> str:
    """
    Analyzes energy usage heatmap data, no history

    Args:
        data: dict: A dictionary containing the following keys:
            - "dates": A dictionary with "start" and "end" dates.
                - "start": Date when the data collection started in 'YYYY-MM-DD' format.
                - "end": Date when the data collection ended in 'YYYY-MM-DD' format.
            - "heatmap": A list of dictionaries, each containing:
                - "day": The day of the week (1 = Sunday, 2 = Monday, ..., 7 = Saturday).
                - "hour": The hour of the day (0 = midnight, 23 = 11 PM).
                - "value": The energy consumption value for the given day and hour. (kWh)
        history: dict: A dictionary containing the same structure as data, but for the previous week.
    """
    if model == "deepseek":
        analyze_page = AnalyzePage(config=deepseek)
    elif model == "gemma":
        analyze_page = AnalyzePage(config=gemma)
    else:
        analyze_page = AnalyzePage(config=gemini)

    try:
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

        start_date = data.get("dates", {}).get("start", "N/A")
        start_date_day = datetime.strptime(start_date, "%Y-%m-%d").strftime("%A")
        start_date_day_number = days.index(start_date_day) + 1
        start_date_complete = f"{start_date_day}, {start_date}"

        end_date = data.get("dates", {}).get("end", "N/A")
        end_date_day = datetime.strptime(end_date, "%Y-%m-%d").strftime("%A")
        end_date_complete = f"{end_date_day}, {end_date}"
        
        start_date_before = history.get("dates", {}).get("start", "N/A")
        end_date_before = history.get("dates", {}).get("end", "N/A")
        start_date_before_complete = f"{start_date_day}, {start_date_before}"
        end_date_before_complete = f"{end_date_day}, {end_date_before}"

        # loop through the heatmap data
        for item in data.get("heatmap", []):
            day_number = item.get("day", "N/A")
            day_name = days[day_number - 1]
            if day_number == start_date_day_number:
                item["date"] = f"{day_name}, {start_date}"
            if day_number > start_date_day_number:
                date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=day_number - start_date_day_number)
                date = date.strftime("%Y-%m-%d")
                item["date"] = f"{day_name}, {date}"
            if day_number < start_date_day_number:
                date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days= 7 - start_date_day_number + day_number)
                date = date.strftime("%Y-%m-%d")
                item["date"] = f"{day_name}, {date}"

        # logger.info(f"↘️ HEATMAP data: {data}")
        # loop through the history data
        for item in history.get("heatmap", []):
            day_number = item.get("day", "N/A")
            day_name = days[day_number - 1]
            if day_number == start_date_day_number:
                item["date"] = f"{day_name}, {start_date_before}"
            if day_number > start_date_day_number:
                date = datetime.strptime(start_date_before, "%Y-%m-%d") + timedelta(days=day_number - start_date_day_number)
                date = date.strftime("%Y-%m-%d")
                item["date"] = f"{day_name}, {date}"
            if day_number < start_date_day_number:
                date = datetime.strptime(start_date_before, "%Y-%m-%d") + timedelta(days= 7 - start_date_day_number + day_number)
                date = date.strftime("%Y-%m-%d")
                item["date"] = f"{day_name}, {date}"

        # logger.info(f"↘️ HEATMAP history: {history}")
        
        #Summarize heatmap, so it can improve more detailed of summary
        hourly_averages = {}
        for item in data.get("heatmap", []):
            date = item.get("date", "N/A")
            hour = item.get("hour", "N/A")
            value = item.get("value", 0.0)
            if hour != "N/A":
                key = f"{date} at {hour}:00"
                if key in hourly_averages:
                    hourly_averages[key]["total"] += value
                    hourly_averages[key]["count"] += 1
                else:
                    hourly_averages[key] = {"total": value, "count": 1}

        # Calculate average for every timeframe.
        for key in hourly_averages:
            hourly_averages[key]["average"] = (
                hourly_averages[key]["total"] / hourly_averages[key]["count"]
            )

        if hourly_averages:
            # find peak average using loop
            peak_value = 0
            low_value = float("inf")

            peak_keys = []
            low_keys = []

            for key in hourly_averages:
                if hourly_averages[key]["average"] > peak_value:
                    peak_keys = [key]
                    peak_value = hourly_averages[key]["average"]
                elif hourly_averages[key]["average"] == peak_value:
                    peak_keys.append(key)

                if hourly_averages[key]["average"] < low_value:
                    low_keys = [key]
                    low_value = hourly_averages[key]["average"]
                elif hourly_averages[key]["average"] == low_value:
                    low_keys.append(key)

            average_overall = (
                sum(item["average"] for item in hourly_averages.values())
                / len(hourly_averages)
            )

        

        #Before calculation on data before
        hourly_averages_before = {}
        for item in history.get("heatmap", []):
            date = item.get("date", "N/A")
            hour = item.get("hour", "N/A")
            value = item.get("value", 0.0)
            if hour != "N/A":
                key = f"{date} at {hour}:00"  # Unique key
                if key in hourly_averages_before:
                    hourly_averages_before[key]["total"] += value
                    hourly_averages_before[key]["count"] += 1
                else:
                    hourly_averages_before[key] = {"total": value, "count": 1}
        
        # Calculate average for every timeframe.
        for key in hourly_averages_before:
            hourly_averages_before[key]["average"] = (
                hourly_averages_before[key]["total"] / hourly_averages_before[key]["count"]
            )

        if hourly_averages_before:
            # find peak average using loop
            peak_value_before = 0
            low_value_before = float("inf")

            peak_keys_before = []
            low_keys_before = []

            for key in hourly_averages_before:
                if hourly_averages_before[key]["average"] > peak_value_before:
                    peak_keys_before = [key]
                    peak_value_before = hourly_averages_before[key]["average"]
                elif hourly_averages_before[key]["average"] == peak_value_before:
                    peak_keys_before.append(key)

                if hourly_averages_before[key]["average"] < low_value_before:
                    low_keys_before = [key]
                    low_value_before = hourly_averages_before[key]["average"]
                elif hourly_averages_before[key]["average"] == low_value_before:
                    low_keys_before.append(key)
            
            average_overall_before = (
                sum(item["average"] for item in hourly_averages_before.values())
                / len(hourly_averages_before)
            )


        if faculty == "":
            faculty = "All faculty"
        if building == "":
            building = "All building"
        if floor == "":
            floor = "All floor"

            

        # get from date
        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        prompt = HEATMAP_PROMPT_TEMPLATE.format(
            current_timestamp=current_timestamp,
            faculty=faculty,
            building=building,
            floor=floor,

            start_date=start_date_complete,
            end_date=end_date_complete,
    
            peak_value=peak_value,
            low_value=low_value,
            peak_keys=peak_keys,
            low_keys=low_keys,
            average_overall=average_overall,

            start_date_before=start_date_before_complete,
            end_date_before=end_date_before_complete,

            peak_value_before=peak_value_before,
            low_value_before=low_value_before,
            peak_keys_before=peak_keys_before,
            low_keys_before=low_keys_before,
            average_overall_before=average_overall_before,
        )

        logger.info(f"↘️ Prompt: {prompt}")
        analysis = await analyze_page._aask(prompt)
        return analysis
    except Exception as e:
        return f"Error generating analysis: {str(e)}"

@cached_analysis("compare_faculty")
async def compare_faculty_analysis(data, history, date, model="") -> str:
    """
    Analyzes energy consumption across faculties, comparing to previous month.
    The history is the result of async_fetch_compare for the previous month.

    Args:
        data: A dictionary containing the following keys:
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
                    - "energy": The total energy consumption in the month. (kWh)
                    - "cost": The total cost associated with the energy consumption in the month. (Rupiah)
                - "average": A dictionary he average energy consumption and cost across all faculties in the month.
                    - "energy": The average energy consumption in the month. (kWh)
                    - "cost": The average cost associated with the energy consumption in the month. (Rupiah)
            - "info": A list of dictionaries, each containing detailed information about a faculty:
                - "faculty": The faculty name. (FTI, FSRD, etc.)
                - "energy": The energy consumption in the month. (kWh)
                - "cost": The cost associated with the energy consumption in the month. (Rupiah)
                - "area": The area of the faculty. (m2)
                - "ike": The energy efficiency index. (kWh/m2)
                - "students": The number of students. 
                - "specific energy": The specific energy consumption per student. (kWh/student)
        history: dict: A dictionary containing the same structure as data.
    """
    if model == "deepseek":
        analyze_page = AnalyzePage(config=deepseek)
    elif model == "gemma":
        analyze_page = AnalyzePage(config=gemma)
    else:
        analyze_page = AnalyzePage(config=gemini)    

    try:
        total_energy = data.get("data", {}).get("total", 0.0)
        min_energy = data.get("data", {}).get("min", {}).get("energy", 0.0)
        max_energy = data.get("data", {}).get("max", {}).get("energy", 0.0)
        
        max_faculty = data.get("data", {}).get("max", {}).get("fakultas", "N/A")
        min_faculty = data.get("data", {}).get("min", {}).get("fakultas", "N/A")
        total_energy_past = history.get("data", {}).get("total", 0.0)

        day_count = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if int(date.split("-")[0]) % 4 == 0 and (int(date.split("-")[0]) % 100 != 0 or int(date.split("-")[0]) % 400 == 0):
            day_count[1] = 29

        month = int(date.split("-")[1])
        prev_month = month - 1
        if prev_month == 0:
            prev_month = 12

        # if current month is the same as current date, then the day count is the current day
        if month == int(datetime.now().strftime("%m")):
            day_count[month-1] = int(datetime.now().strftime("%d"))
        
        avg_energy_per_day_max=max_energy/day_count[month-1]
        avg_energy_per_day_min=min_energy/day_count[month-1]
        avg_energy_per_day=total_energy["total"]/day_count[month-1]
        avg_cost_per_day=total_energy["cost"]/day_count[month-1]
        avg_energy_per_day_past=total_energy_past["total"]/day_count[prev_month-1]
        avg_cost_per_day_past=total_energy_past["cost"]/day_count[prev_month-1]

        # get from date
        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        prompt = COMPARE_FACULTY_PROMPT_TEMPLATE.format(
            current_timestamp=current_timestamp,
            date=date,
            min_energy=min_energy,
            min_faculty=min_faculty,
            max_energy=max_energy,
            max_faculty=max_faculty,
            total_usage=total_energy["total"],
            total_cost=total_energy["cost"],
            total_usage_past=total_energy_past["total"],
            total_cost_past=total_energy_past["cost"],
            avg_energy_per_day_max=avg_energy_per_day_max,
            avg_energy_per_day_min=avg_energy_per_day_min,
            avg_energy_per_day=avg_energy_per_day,
            avg_cost_per_day=avg_cost_per_day,
            avg_energy_per_day_past=avg_energy_per_day_past,
            avg_cost_per_day_past=avg_cost_per_day_past,
        )

        logger.info(f"↘️ Prompt: {prompt}")
        analysis = await analyze_page._aask(prompt)
        return analysis
    except Exception as e:
        return f"Error generating analysis: {str(e)}"