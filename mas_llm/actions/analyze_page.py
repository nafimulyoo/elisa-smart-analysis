from metagpt.actions import Action



class AnalyzePage(Action):
    name: str = "AnalyzePage"

    async def run(self, mode, data, history):

        if mode == "now":
            response = await now_analysis(data, history)
            return response
        elif mode == "daily":
            response = await daily_analysis(data, history)
            return response
        elif mode == "monthly":
            response = await monthly_analysis(data, history)
            return response
        elif mode == "heatmap":
            response = await heatmap_analysis(data, history)
            return response
        elif mode == "compare_faculty":
            response = await compare_faculty_analysis(data, history)
            return response
        
analyze_page = AnalyzePage()


async def now_analysis(data, history) -> str:
    """Analyzes real-time energy data, comparing against a heatmap for the past week.
        history is the result of async_fetch_heatmap
    """
    PROMPT_TEMPLATE = """
    You are an energy data analyst. Analyze the current power consumption data in the context of the past week's energy usage heatmap.
    Provide a concise summary (2-3 sentences) highlighting any significant deviations from the typical pattern and potential causes.
    Emphasize actionable insights and compare current data to the trends visible in the heatmap. 

    Current Data:
    Current Timestamp: {current_timestamp}
    Current Power Consumption (kW): {current_power}

    Heatmap Summary (Past Week):
    {heatmap_summary}

    Analysis (use Bahasa Indonesia) summary (2-3 sentences):
    """



    try:
        # Extract Current Data
        chart_data = data.get("chart_data", [])
        current_timestamp = (
            chart_data[-1].get("timestamp", "N/A") if chart_data else "N/A"
        )
        current_power = chart_data[-1].get("power", 0.0) if chart_data else 0.0

        # Summarize Heatmap Data
        heatmap_summary = "No heatmap data available."
        if history and history.get("heatmap"):
            heatmap_data = history["heatmap"]
            # Calculate averages for each hour, summarize key patterns
            hourly_averages = {}
            for item in heatmap_data:
                day = item.get("day", "N/A")
                hour = item.get("hour", "N/A")
                value = item.get("value", 0.0)
                if hour != "N/A":
                    key = f"{day}-{hour}"  # Unique key
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

                peak_days = [key.split("-")[0] for key in peak_keys]
                peak_hours = [key.split("-")[1] for key in peak_keys]

                low_days = [key.split("-")[0] for key in low_keys]
                low_hours = [key.split("-")[1] for key in low_keys]

                peak_string = (
                    f"Peak Value was Day: {', '.join(peak_days)} Hour:"
                    f" {', '.join(peak_hours)} Value: {peak_value} "
                )

                low_string = (
                    f"Low value was Day: {', '.join(low_days)} Hour:"
                    f" {', '.join(low_hours)} Value: {low_value}"
                )

                heatmap_summary = (
                    f"""The heatmap shows the peak was {peak_string}.
                                        The low was {low_string}.
                                        Overall average was {average_overall}"""
                )

        prompt = PROMPT_TEMPLATE.format(
            current_timestamp=current_timestamp,
            current_power=current_power,
            heatmap_summary=heatmap_summary,
        )

        analysis = await analyze_page._aask(prompt)
        return analysis

    except Exception as e:
        return f"Error generating analysis: {str(e)}"


async def daily_analysis(data, history) -> str:
    """Analyzes daily energy data, comparing it to a heatmap of the past week.
        history is the result of async_fetch_heatmap.
    """
    PROMPT_TEMPLATE = """
    You are an energy data analyst. Analyze the daily energy consumption data in the context of the past week's energy usage heatmap.
    Provide a concise summary (3-4 sentences) including peak usage hours, phase imbalances, and how today's consumption compares to the patterns in the heatmap.
    Indicate if today's energy use is anomalous, based on what is typical in the heatmap.

    Daily Data:
    Date: {date}
    Total Energy Consumption (kWh): {total_energy}
    Peak Usage Hours: {peak_hours}
    Phase R Consumption: {phase_r}
    Phase S Consumption: {phase_s}
    Phase T Consumption: {phase_t}

    Heatmap Summary (Past Week):
    {heatmap_summary}

    Analysis (use Bahasa Indonesia) summary (2-3 sentences):
    """



    try:
        # Extract Daily Data
        today_data = data.get("today_data", {})
        date_obj = data.get("date", "N/A")
        total_energy = today_data.get("total_daya", 0.0)

        # Peak Hours has been reformatted here,
        peak_hours = []
        for data_hourly in data.get("hourly_data", []):
            peak_hours.append(
                f"{data_hourly.get('hour')} - {data_hourly.get('energy')}"
            )

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

        # Summarize Heatmap Data
        heatmap_summary = "No heatmap data available."
        if history and history.get("heatmap"):
            heatmap_data = history["heatmap"]
            # Calculate averages for each hour, summarize key patterns
            hourly_averages = {}
            for item in heatmap_data:
                day = item.get("day", "N/A")
                hour = item.get("hour", "N/A")
                value = item.get("value", 0.0)
                if hour != "N/A":
                    key = f"{day}-{hour}"  # Unique key
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

                peak_days = [key.split("-")[0] for key in peak_keys]
                peak_hours = [key.split("-")[1] for key in peak_keys]

                low_days = [key.split("-")[0] for key in low_keys]
                low_hours = [key.split("-")[1] for key in low_keys]

                peak_string = (
                    f"Peak Value was Day: {', '.join(peak_days)} Hour:"
                    f" {', '.join(peak_hours)} Value: {peak_value} "
                )

                low_string = (
                    f"Low value was Day: {', '.join(low_days)} Hour:"
                    f" {', '.join(low_hours)} Value: {low_value}"
                )

                heatmap_summary = (
                    f"""The heatmap shows the peak was {peak_string}.
                                        The low was {low_string}.
                                        Overall average was {average_overall}"""
                )

        prompt = PROMPT_TEMPLATE.format(
            date=date_obj,
            total_energy=total_energy,
            peak_hours=peak_hours,
            phase_r=phase_r,
            phase_s=phase_s,
            phase_t=phase_t,
            heatmap_summary=heatmap_summary,
        )
        analysis = await analyze_page._aask(prompt)
        return analysis
    except Exception as e:
        return f"Error generating analysis: {str(e)}"


async def monthly_analysis(data, history) -> str:
    """Analyzes monthly energy data, comparing to a list of previous months.

    Args:
        data (Dict[str, Any]):  Current month's data (result of async_fetch_monthly).
        history (List[Dict[str, Any]]): List of up to 3 previous months' data, each a result of async_fetch_monthly.
    """
    PROMPT_TEMPLATE = """
    You are an energy data analyst. Analyze the monthly energy consumption data, comparing to recent months.
    Provide a summary (3-4 sentences) highlighting total consumption, peak days, phase contribution, and anomaly detection based on historical data.
    Quantify trends vs historical averages, show insights what are different now, vs history and what you can improve.

    Data:
    Month: {month}
    Total Energy Consumption (kWh): {total_energy}
    Peak Consumption Days: {peak_days}
    Phase 1 Contribution (%): {phase1_contribution}
    Phase 2 Contribution (%): {phase2_contribution}
    Phase 3 Contribution (%): {phase3_contribution}

    Historical Context:
    {historical_summary}

    Analysis (use Bahasa Indonesia) summary (2-3 sentences):
    """



    try:
        month = data.get("date", "N/A")
        month_data = data.get("month_data", {})
        total_energy = month_data.get("total_daya", 0.0)
        daily_data = data.get("daily_data", [])

        #Peakdays is on timestamp format on the JSON so change it
        peak_days_string = []
        for day in daily_data:
            peak_days_string.append(f"{day.get('timestamp')} - {day.get('energy')}")
        peak_days = ", ".join(peak_days_string)

        # Phase Contribution
        phase1_total = sum(day.get("phase 1", 0.0) for day in daily_data)
        phase2_total = sum(day.get("phase 2", 0.0) for day in daily_data)
        phase3_total = sum(day.get("phase 3", 0.0) for day in daily_data)
        total_phase = phase1_total + phase2_total + phase3_total

        phase1_contribution = (phase1_total / total_phase) * 100 if total_phase else 0
        phase2_contribution = (phase2_total / total_phase) * 100 if total_phase else 0
        phase3_contribution = (phase3_total / total_phase) * 100 if total_phase else 0

        phase1_contribution = round(phase1_contribution, 2)
        phase2_contribution = round(phase2_contribution, 2)
        phase3_contribution = round(phase3_contribution, 2)

        # Summarize Historical Data
        historical_summary = "No historical data available."
        if history:
            historical_consumptions = []
            for i, h in enumerate(history):
                if h and h.get("month_data"):
                    historical_consumptions.append(h["month_data"].get("total_daya", 0.0))
                else:
                    historical_consumptions.append(0.0)  # Missing value

            #Now with the new function, find the average consumptions
            if len(historical_consumptions) == 3:
                average_consumptions = sum(historical_consumptions) / len(
                    historical_consumptions
                )
            else:
                average_consumptions = 0
            historical_summary = f"Average historical consumption (past months): {average_consumptions:.2f} kWh"

        prompt = PROMPT_TEMPLATE.format(
            month=month,
            total_energy=total_energy,
            peak_days=peak_days,
            phase1_contribution=phase1_contribution,
            phase2_contribution=phase2_contribution,
            phase3_contribution=phase3_contribution,
            historical_summary=historical_summary,
        )
        analysis = await analyze_page._aask(prompt)
        return analysis
    except Exception as e:
        return f"Error generating analysis: {str(e)}"


async def heatmap_analysis(data, history) -> str:
    """Analyzes heatmap data. No historical comparison needed for this example.
        history should be an empty dictionary - will not be used.
    """
    PROMPT_TEMPLATE = """
    You are an energy data analyst. Analyze the energy usage heatmap data and identify key patterns.
    Provide a summary (3-4 sentences) highlighting the days of the week and hours of the day with the highest and lowest consumption, and any significant anomalies.

    Current Heatmap Data:
    Start Date: {start_date}
    End Date: {end_date}
    Data: {data}

    Week Before Heatmap Data:
    Start Date: {start_date_before}
    End Date: {end_date_before}
    Data: {data_before}

    Analysis (use Bahasa Indonesia) summary (2-3 sentences):
    """



    try:
        start_date = data.get("dates", {}).get("start", "N/A")
        end_date = data.get("dates", {}).get("end", "N/A")
        
        start_date_before = history.get("dates", {}).get("start", "N/A")
        end_date_before = history.get("dates", {}).get("end", "N/A")

        prompt = PROMPT_TEMPLATE.format(
            start_date=start_date,
            end_date=end_date,
            data=data,
            start_date_before=start_date_before,
            end_date_before=end_date_before,
            data_before=history
        )

        analysis = await analyze_page._aask(prompt)
        return analysis
    except Exception as e:
        return f"Error generating analysis: {str(e)}"


async def compare_faculty_analysis(data, history) -> str:
    """Analyzes energy consumption across faculties, comparing to historical averages.

        The History parameter should be async_fetch_compare with the historical month
    """
    PROMPT_TEMPLATE = """
    You are an energy data analyst. Analyze the energy consumption data for different faculties and identify key differences.
    Provide a summary (3-4 sentences) ranking the faculties by energy consumption, highlighting those with significantly higher or lower consumption than the average.
    Compare current faculty consumptions to historical faculty consumptions and point out changes and potential insights.

    Data:
    Date: {date}
    Faculty with lowest usage: {max_energy}
    Faculty with lowest usage: {min_energy}
    Total energy usage: {total_usage}
    Average Energy Consumption across all faculties (kWh): {average_energy}
    Change vs historical : {change_vs_history}

    Analysis (use Bahasa Indonesia) summary (2-3 sentences):
    """



    try:
        total_energy = data.get("data", {}).get("total", 0.0)
        min_energy = data.get("data", {}).get("min", 0.0)
        max_energy = data.get("data", {}).get("max", 0.0)
        average_energy = data.get("data", {}).get("average", {}).get("energy", 0.0)
        date = data.get("date", "N/A")
        change_vs_history = 0.0

        #Compare History so we can provide more insights to the prompt
        if history and history.get("data", {}).get("average", {}).get("energy", 0.0):
            historical_energy = history["data"]["average"]["energy"]

            change_vs_history = average_energy - historical_energy
        else:
            change_vs_history = 0.0

        prompt = PROMPT_TEMPLATE.format(
            date=date,
            average_energy=average_energy,
            change_vs_history=change_vs_history,
            min_energy=min_energy,
            max_energy=max_energy,
            total_usage=total_energy
        )

        analysis = await analyze_page._aask(prompt)
        return analysis
    except Exception as e:
        return f"Error generating analysis: {str(e)}"