NOW_PROMPT_TEMPLATE = """
# Instruction
You are an energy data analyst. Your task is to analyze real-time power consumption this hour and compare it to past month data (considered to be of equal, higher, or lower) (Don't compare using total energy usage, or total cost, but rather the cost per hour and average power), suggesting causes, and highlight any anomalies. Give context to the location and time, look at data date and current timestamp. Say the year/month/date/time of the data, if its same as current year/month/date/time (current timestamp), say this year/month/date/time. Format numbers with titik as thousands separator and koma as decimal separator. When relevant, use Rupiah currency format. High usage is measured relative to the average power per hour last month, and low usage is measured relative to the average usage per hour last month.

## Current Timestamp: 2025-03-31 22:56:32
## Location:
Faculty: FTI
Building: LABTEK VI
Floor: 
## Data:
Date: 2025-03-01

### Last 1 Hour Data:
Measurement Start Time: 2025-03-31 21:57:00
Measurement End Time: 2025-03-31 22:55:00
Latest Power: 8.36 kW.
Max Power: 9.54 kW, Time: 2025-03-31 22:28:00
Min Power: 8.34 kW, Time: 2025-03-31 22:51:00

### This Day Data:
Total Energy Today: 183.6 kWh
Avg Power Today: 7.98 kW

Total Cost Today: Rp195551,00
Avg Cost Per Hour Today: Rp8502,00 

### Past Month Data:
Total Energy Last Month: 16764.27 kWh
Avg Energy Per Day Last Month: 598.72 kWh
Avg Power Last Month: 24.95 kW

Total Cost Last Month: Rp17351291,00
Avg Cost Per Day Last Month: Rp619688,00
Avg Cost Per Hour Last Month: Rp25820,00
## You Analysis without any intro (Bahasa Indonesia, 5 kalimat):
Konsumsi daya terkini (8,36 kW) pada tanggal 31 Maret 2025 pukul 22:55:00 lebih rendah dibandingkan rata-rata per jam bulan lalu (24,95 kW). Biaya rata-rata per jam hari ini Rp8.502,00 juga lebih rendah dibandingkan rata-rata biaya per jam bulan lalu Rp25.820,00. Hal ini menunjukkan penurunan signifikan dalam penggunaan energi di LABTEK VI FTI. Perbedaan antara daya minimum (8,34 kW) dan maksimum (9,54 kW) dalam satu jam terakhir relatif kecil, menunjukkan konsumsi daya yang stabil. Tidak ada indikasi anomali yang mencolok pada data hari ini.

# You Analysis Task
## Current Timestamp: {current_timestamp}
## Location:
Faculty: {faculty}
Building: {building}
Floor: {floor}
## Data:
### Last 1 Hour Data:
Measurement Start Time: {measurement_start_time}
Measurement End Time: {measurement_end_time}
Latest Power: {current_power} kW.
Max Power: {max_power} kW, Time: {max_timestamp}
Min Power: {min_power} kW, Time: {min_timestamp}

### This Day Data:
Total Energy Today: {total_power_today} kWh
Avg Power Today: {avg_power_per_hour_today} kW

Total Cost Today: Rp{total_cost_today},00
Avg Cost Per Hour Today: Rp{avg_cost_per_hour_today},00 

### Past Month Data:
Total Energy Last Month: {total_power_prev_month} kWh
Avg Energy Per Day Last Month: {avg_power_per_day_prev_month} kWh
Avg Power Last Month: {avg_power_per_hour_prev_month} kW

Total Cost Last Month: Rp{total_cost_prev_month},00
Avg Cost Per Day Last Month: Rp{avg_cost_per_day_prev_month},00
Avg Cost Per Hour Last Month: Rp{avg_cost_per_hour_prev_month},00
## You Analysis without any intro (Bahasa Indonesia, 5 kalimat):
"""



DAILY_PROMPT_TEMPLATE = """
# Instruction
You are an energy data analyst. Your task is to analyze daily energy consumption in the required day, compare it to past month data (considered to be of equal, higher, or lower)  (Don't compare using total power, or total cost, but rather the average power and cost per hour), suggesting causes, and highlight any anomalies. Give context to the location and time, look at data date and current timestamp. Say the year/month/date/time of the data, if its same as current year/month/date/time (current timestamp), say this year/month/date/time. Format numbers with titik as thousands separator and koma as decimal separator. When relevant, use Rupiah currency format.

# Example
## Current Timestamp: 2025-04-01 00:28:57
## Location:
Faculty: FTI
Building: LABTEK VI
Floor: All floor
## Data: 
### Date: 2025-03-01
Total Energy Consumption: 399.17 kWh
Total Cost: Rp424815,00
Average Power: 16.63 kW
Average Cost per Hour: Rp17700,00
Max Usage: 21.18 kWh at 2025-03-01 12:00:00
Min Usage: 13.37 kWh at 2025-03-01 02:00:00
Phase R Consumption: 149.84 kWh
Phase S Consumption: 141.91 kWh
Phase T Consumption: 107.39 kWh
### Previous Month Data:
Total Month Energy Consumption: 16764.27 kWh
Total Month Cost: Rp17351291,00
Average Daily Energy Consumption: 598.72 kWh
Average Daily Cost: Rp619688,00
Average Power: 24.94 kW
Average Cost per Hour: Rp25820,00

## You Analysis without any intro (Bahasa Indonesia, 4 kalimat):
Analisis konsumsi energi pada tanggal 1 Maret 2025 di LABTEK VI FTI menunjukkan rata-rata daya 16,63 kW dan biaya per jam Rp17.700,00, yang lebih rendah dibandingkan rata-rata bulan sebelumnya (24,95 kW dan Rp25.820,33 per jam). Kemungkinan penyebabnya adalah tingkat aktivitas yang lebih rendah pada tanggal tersebut dibandingkan rata-rata harian bulan sebelumnya. Tidak ada anomali signifikan terlihat, namun perlu diperhatikan ketidakseimbangan konsumsi antar fase (R, S, dan T).

# Your Analysis Task
## Current Timestamp: {current_timestamp}
## Location:
Faculty: {faculty}
Building: {building}
Floor: {floor}
## Data: 
### Date: {date}
Total Energy Consumption: {total_energy} kWh
Total Cost: Rp{total_cost},00
Average Power: {avg_power} kW
Average Cost per Hour: Rp{avg_cost_per_hour},00
Max Usage: {max_energy} kWh at {max_timestamp}
Min Usage: {min_energy} kWh at {min_timestamp}
Phase R Consumption: {phase_r} kWh
Phase S Consumption: {phase_s} kWh
Phase T Consumption: {phase_t} kWh
### Previous Month Data:
Total Month Energy Consumption: {total_month_energy_prev_month} kWh
Total Month Cost: Rp{total_month_cost_prev_month},00
Average Daily Energy Consumption: {total_day_energy_prev_month} kWh
Average Daily Cost: Rp{total_day_cost_prev_month},00
Average Power: {avg_power_prev_month} kW
Average Cost per Hour: Rp{avg_cost_per_hour_prev_month},00

## You Analysis without any intro (Bahasa Indonesia, 4 kalimat):
"""

MONTHLY_PROMPT_TEMPLATE = """
# Instruction
You are an energy data analyst. Your task is to analyze monthly energy consumption in the required month, compare it to past month data (considered to be of equal, higher, or lower)  (Don't compare using total power, or total cost, but rather the average power and cost per hour), suggesting causes, and highlight any anomalies. Give context to the location and time, look at data date and current timestamp. Say the year/month/date/time of the data, if its same as current year/month/date/time (current timestamp), say this year/month/date/time. Format numbers with titik as thousands separator and koma as decimal separator. When relevant, use Rupiah currency format.

# Example
## Current Timestamp: 2025-04-01 00:33:34
## Location:
Faculty: FTI
Building: LABTEK VI
Floor: All floor
## Data: 
### Month: 2025-02
Total Energy Consumption: 16764.27 kWh
Total Cost: Rp17351291,00
Average Daily Energy Consumption: 598.72 kWh
Average Daily Cost: Rp619688,00
Max Usage: 774.18 kWh at 2025-02-25 00:00:00
Min Usage: 383.7 kWh at 2025-02-02 00:00:00
Phase R Consumption: 5977.280000000001 kWh
Phase S Consumption: 6172.400000000001 kWh
Phase T Consumption: 4614.6 kWh
### Previous Month Data:
Total Month Energy Consumption: 18897.92 kWh
Total Month Cost: Rp19606900,00
Average Daily Energy Consumption: 609.61 kWh
Average Daily Cost: Rp632480,00
## You Analysis without any intro (Bahasa Indonesia, 4 kalimat):
Analisis konsumsi energi bulan Februari 2025 di LABTEK VI FTI menunjukkan penurunan dibandingkan bulan sebelumnya. Rata-rata konsumsi harian turun dari 609,61 kWh menjadi 598,72 kWh, dan biaya harian juga turun dari Rp632.480,00 menjadi Rp619.688,00. Penurunan ini mungkin disebabkan oleh berkurangnya aktivitas perkuliahan atau efisiensi penggunaan energi. Tidak ada anomali signifikan, namun perlu diperhatikan perbedaan konsumsi antar fase, dimana fase T lebih rendah dibandingkan fase R dan S.

# Your Analysis Task
## Current Timestamp: {current_timestamp}
## Location:
Faculty: {faculty}
Building: {building}
Floor: {floor}
## Data: 
### Month: {date}
Total Energy Consumption: {total_energy} kWh
Total Cost: Rp{total_cost},00
Average Daily Energy Consumption: {avg_power} kWh
Average Daily Cost: Rp{avg_cost_per_day},00
Max Usage: {max_energy} kWh at {max_timestamp}
Min Usage: {min_energy} kWh at {min_timestamp}
Phase R Consumption: {phase_r} kWh
Phase S Consumption: {phase_s} kWh
Phase T Consumption: {phase_t} kWh
### Previous Month Data:
Total Month Energy Consumption: {total_month_energy_prev_month} kWh
Total Month Cost: Rp{total_month_cost_prev_month},00
Average Daily Energy Consumption: {total_day_energy_prev_month} kWh
Average Daily Cost: Rp{total_day_cost_prev_month},00

## You Analysis without any intro (Bahasa Indonesia, 4 kalimat):
"""

HEATMAP_PROMPT_TEMPLATE = """
# Instruction
You are an energy data analyst. Your task is to analyze energy usage heatmap data, identify key patterns, and highlight the highest/lowest consumption periods, comparing it to past week data (considered to be of equal, higher, or lower), suggesting causes, and highlight any anomalies.Give context to the location and time, look at data date and current timestamp. Say the year/month/date/time of the data, if its same as current year/month/date/time (current timestamp), say this year/month/date/time. Be very spesific on date (ex: Kamis, 27 Maret 2025). Format numbers with titik as thousands separator and koma as decimal separator. When relevant, use Rupiah currency format. timestamp).

# Example:
## Current Timestamp: 2025-04-01 12:24:46
## Location:
Faculty: FTI
Building: LABTEK VI
Floor: All floor
## Data: 
Start Date: Saturday, 2025-03-01
End Date: Friday, 2025-03-07
Peak Average Hours: 68.37 kW at ['Tuesday, 2025-03-04 at 13:00']
Low Average Hours: 13.36 kW at ['Saturday, 2025-03-01 at 2:00']
Overall Average: 26.413869047619055 kW
## Past Week Data:
Start Date: Saturday, 2025-02-22
End Date: Friday, 2025-02-28
Peak Average Hours: 60.21 kW at ['Tuesday, 2025-02-25 at 14:00']
Low Average Hours: 14.13 kW at ['Friday, 2025-02-28 at 23:00']
Overall Average: 26.452916666666667 kW
## You Analysis without any intro (Bahasa Indonesia, 3 kalimat):
Analisis data penggunaan energi di LABTEK VI FTI dari tanggal 1 Maret 2025 hingga 7 Maret 2025 menunjukkan puncak konsumsi rata-rata sebesar 68,37 kW pada hari Selasa, 4 Maret 2025 pukul 13:00 dan konsumsi terendah 13,36 kW pada hari Sabtu, 1 Maret 2025 pukul 02:00. Dibandingkan dengan minggu sebelumnya (22 Februari 2025 - 28 Februari 2025), puncak penggunaan energi meningkat dari 60,21 kW, sementara konsumsi terendah sedikit menurun dari 14,13 kW, dengan rata-rata keseluruhan yang hampir sama. Peningkatan puncak konsumsi ini, terutama pada hari Selasa, perlu ditelusuri lebih lanjut untuk mengidentifikasi aktivitas atau peralatan spesifik yang menyebabkan lonjakan tersebut.

# Your Analysis Task
## Current Timestamp: {current_timestamp}
## Location:
Faculty: {faculty}
Building: {building}
Floor: {floor}
## Data: 
Start Date: {start_date}
End Date: {end_date}
Peak Average Hours: {peak_value} kW at {peak_keys}
Low Average Hours: {low_value} kW at {low_keys}
Overall Average: {average_overall} kW
## Past Week Data:
Start Date: {start_date_before}
End Date: {end_date_before}
Peak Average Hours: {peak_value_before} kW at {peak_keys_before}
Low Average Hours: {low_value_before} kW at {low_keys_before}
Overall Average: {average_overall_before} kW
## You Analysis without any intro (Bahasa Indonesia, 3 kalimat):
"""

COMPARE_FACULTY_PROMPT_TEMPLATE = """
# Instruction
You are an energy data analyst. Your task is to analyze energy consumption across faculties, identify key differences, rank faculties by consumption, and highlight any significant changes, comparing it to past month data (considered to be of equal, higher, or lower). Give context to time, look at data date and current timestamp. Say the month and year of the data, if its same as current month (current timestamp), say this month. Format numbers with titik as thousands separator and koma as decimal separator. When relevant, use Rupiah currency format. If the data month is not the same as current month and lower than previous month, say because its because its still in the middle of the month. If its still not in the end of the month (before the 25th), don't compare by the total, but rather the average power and cost per day.

# Example
## Current Timestamp: 2025-04-01 13:34:28
## Data: 
Date: 2025-04

Faculty with Maximum Usage: FTMD with 2092.29 kWh and average per day 2092.29 kWh
Faculty with Minimum Usage: SITH with 22.2 kWh and average per day 22.2 kWh

Total Energy Usage This Month: 8658.44 kWh and average per day 8658.44 kWh
Total Energy Cost This Month Rp8268809,00 and average per day Rp8268809.0,00

Total Energy Usage Past Month: 675029.21 kWh and average per day 21775.135806451613 kWh
Total Energy Cost Past Month: Rp698156866,00 and average per day Rp22521189.225806452,00
## You Analysis without any intro (Bahasa Indonesia, 4 kalimat):
FTMD mencatat penggunaan energi tertinggi sebesar 2.092,29 kWh dengan rata-rata 2.092,29 kWh per hari, sementara SITH memiliki penggunaan terendah yaitu 22,2 kWh dengan rata-rata 22,2 kWh per hari. Total penggunaan energi bulan April 2025 adalah 8.658,44 kWh (Rp8.268.809,00) dengan rata-rata per hari 8.658,44 kWh (Rp8.268.809,00). Karena ini masih awal bulan April, konsumsi energi jauh lebih rendah dibandingkan bulan Maret (675.029,21 kWh atau Rp698.156.866,00), dengan rata-rata penggunaan energi per hari bulan April juga lebih rendah dibandingkan bulan Maret.

# You Analysis Task
## Current Timestamp: {current_timestamp}
## Data: 
Date: {date}

Faculty with Maximum Usage: {max_faculty} with {max_energy} kWh and average per day {avg_energy_per_day_max} kWh
Faculty with Minimum Usage: {min_faculty} with {min_energy} kWh and average per day {avg_energy_per_day_min} kWh

Total Energy Usage This Month: {total_usage} kWh and average per day {avg_energy_per_day} kWh
Total Energy Cost This Month Rp{total_cost},00 and average per day Rp{avg_cost_per_day},00

Total Energy Usage Past Month: {total_usage_past} kWh and average per day {avg_energy_per_day_past} kWh
Total Energy Cost Past Month: Rp{total_cost_past},00 and average per day Rp{avg_cost_per_day_past},00
## You Analysis without any intro (Bahasa Indonesia, 4 kalimat):
"""
