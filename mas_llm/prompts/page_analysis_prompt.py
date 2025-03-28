NOW_PROMPT_TEMPLATE = """
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

DAILY_PROMPT_TEMPLATE = """
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

MONTHLY_PROMPT_TEMPLATE = """
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

HEATMAP_PROMPT_TEMPLATE = """
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

COMPARE_FACULTY_PROMPT_TEMPLATE = """
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

