NOW_PROMPT_TEMPLATE = """
# Instruksi
Anda adalah seorang analis data energi. Tugas Anda adalah menganalisis konsumsi daya real-time pada jam ini dan membandingkannya dengan data bulan lalu (dianggap sama, lebih tinggi, atau lebih rendah) (Jangan membandingkan menggunakan total penggunaan energi, atau total biaya, tetapi biaya per jam dan daya rata-rata), menyarankan penyebabnya, dan menyoroti setiap anomali. Berikan konteks lokasi dan waktu, perhatikan tanggal data dan timestamp saat ini. Sebutkan tahun/bulan/tanggal/waktu data, jika sama dengan tahun/bulan/tanggal/waktu saat ini (timestamp saat ini), sebutkan tahun/bulan/tanggal/waktu ini. Format angka dengan titik sebagai pemisah ribuan dan koma sebagai pemisah desimal. Jika relevan, gunakan format mata uang Rupiah. Penggunaan tinggi diukur relatif terhadap daya rata-rata per jam bulan lalu, dan penggunaan rendah diukur relatif terhadap penggunaan rata-rata per jam bulan lalu. Bulatkan hingga 2 angka desimal untuk semua angka.

## Timestamp Saat Ini: 2025-03-31 22:56:32
## Lokasi:
Fakultas: FTI
Gedung: LABTEK VI
Lantai:
## Data:
Tanggal: 2025-03-01

### Data 1 Jam Terakhir:
Waktu Mulai Pengukuran: 2025-03-31 21:57:00
Waktu Selesai Pengukuran: 2025-03-31 22:55:00
Daya Terkini: 8,36 kW.
Daya Maksimum: 9,54 kW, Waktu: 2025-03-31 22:28:00
Daya Minimum: 8,34 kW, Waktu: 2025-03-31 22:51:00

### Data Hari Ini:
Total Energi Hari Ini: 183,6 kWh
Rata-rata Daya Hari Ini: 7,98 kW

Total Biaya Hari Ini: Rp195.551,00
Rata-rata Biaya Per Jam Hari Ini: Rp8.502,00

### Data Bulan Lalu:
Total Energi Bulan Lalu: 16.764,27 kWh
Rata-rata Energi Per Hari Bulan Lalu: 598,72 kWh
Rata-rata Daya Bulan Lalu: 24,95 kW

Total Biaya Bulan Lalu: Rp17.351.291,00
Rata-rata Biaya Per Hari Bulan Lalu: Rp619.688,00
Rata-rata Biaya Per Jam Bulan Lalu: Rp25.820,00
## Analisis Anda tanpa intro (Bahasa Indonesia, 5 kalimat, seperti contoh):
Konsumsi daya terkini (8,36 kW) pada tanggal 31 Maret 2025 pukul 22:55:00 lebih rendah dibandingkan rata-rata per jam bulan lalu (24,95 kW). Biaya rata-rata per jam hari ini Rp8.502,00 juga lebih rendah dibandingkan rata-rata biaya per jam bulan lalu Rp25.820,00. Hal ini menunjukkan penurunan signifikan dalam penggunaan energi di LABTEK VI FTI. Perbedaan antara daya minimum (8,34 kW) dan maksimum (9,54 kW) dalam satu jam terakhir relatif kecil, menunjukkan konsumsi daya yang stabil. Tidak ada indikasi anomali yang mencolok pada data hari ini.

# Tugas Analisis Anda
## Timestamp Saat Ini: {current_timestamp}
## Lokasi:
Fakultas: {faculty}
Gedung: {building}
Lantai: {floor}
## Data:
### Data 1 Jam Terakhir:
Waktu Mulai Pengukuran: {measurement_start_time}
Waktu Selesai Pengukuran: {measurement_end_time}
Daya Terkini: {current_power} kW.
Daya Maksimum: {max_power} kW, Waktu: {max_timestamp}
Daya Minimum: {min_power} kW, Waktu: {min_timestamp}

### Data Hari Ini:
Total Energi Hari Ini: {total_power_today} kWh
Rata-rata Daya Hari Ini: {avg_power_per_hour_today} kW

Total Biaya Hari Ini: Rp{total_cost_today},00
Rata-rata Biaya Per Jam Hari Ini: Rp{avg_cost_per_hour_today},00

### Data Bulan Lalu:
Total Energi Bulan Lalu: {total_power_prev_month} kWh
Rata-rata Energi Per Hari Bulan Lalu: {avg_power_per_day_prev_month} kWh
Rata-rata Daya Bulan Lalu: {avg_power_per_hour_prev_month} kW

Total Biaya Bulan Lalu: Rp{total_cost_prev_month},00
Rata-rata Biaya Per Hari Bulan Lalu: Rp{avg_cost_per_day_prev_month},00
Rata-rata Biaya Per Jam Bulan Lalu: Rp{avg_cost_per_hour_prev_month},00
## Analisis Anda tanpa intro (Bahasa Indonesia, 5 kalimat, seperti contoh):
"""

DAILY_PROMPT_TEMPLATE = """
# Instruksi
Anda adalah seorang analis data energi. Tugas Anda adalah menganalisis konsumsi energi harian pada hari yang diminta, membandingkannya dengan data bulan lalu (dianggap sama, lebih tinggi, atau lebih rendah) (Jangan membandingkan menggunakan total daya, atau total biaya, tetapi daya rata-rata dan biaya per jam), menyarankan penyebabnya, dan menyoroti setiap anomali. Berikan konteks lokasi dan waktu, perhatikan tanggal data dan timestamp saat ini. Sebutkan tahun/bulan/tanggal/waktu data, jika sama dengan tahun/bulan/tanggal/waktu saat ini (timestamp saat ini), sebutkan tahun/bulan/tanggal/waktu ini. Format angka dengan titik sebagai pemisah ribuan dan koma sebagai pemisah desimal. Jika relevan, gunakan format mata uang Rupiah. Bulatkan hingga 2 angka desimal untuk semua angka.

# Contoh
## Timestamp Saat Ini: 2025-04-01 00:28:57
## Lokasi:
Fakultas: FTI
Gedung: LABTEK VI
Lantai: Semua lantai
## Data:
### Tanggal: 2025-03-01
Total Konsumsi Energi: 399,17 kWh
Total Biaya: Rp424.815,00
Rata-rata Daya: 16,63 kW
Rata-rata Biaya per Jam: Rp17.700,00
Penggunaan Maksimum: 21,18 kWh pada 2025-03-01 12:00:00
Penggunaan Minimum: 13,37 kWh pada 2025-03-01 02:00:00
Konsumsi Fase R: 149,84 kWh
Konsumsi Fase S: 141,91 kWh
Konsumsi Fase T: 107,39 kWh
### Data Bulan Sebelumnya:
Total Konsumsi Energi Bulan: 16.764,27 kWh
Total Biaya Bulan: Rp17.351.291,00
Rata-rata Konsumsi Energi Harian: 598,72 kWh
Rata-rata Biaya Harian: Rp619.688,00
Rata-rata Daya: 24,94 kW
Rata-rata Biaya per Jam: Rp25.820,00

## Analisis Anda tanpa intro (Bahasa Indonesia, 1 paragraf berisi 4 kalimat, seperti contoh):
Analisis konsumsi energi pada tanggal 1 Maret 2025 di LABTEK VI FTI menunjukkan rata-rata daya 16,63 kW dan biaya per jam Rp17.700,00, yang lebih rendah dibandingkan rata-rata bulan sebelumnya (24,95 kW dan Rp25.820,00 per jam). Kemungkinan penyebabnya adalah tingkat aktivitas yang lebih rendah pada tanggal tersebut dibandingkan rata-rata harian bulan sebelumnya. Tidak ada anomali signifikan terlihat, namun perlu diperhatikan ketidakseimbangan konsumsi antar fase (R, S, dan T).

# Tugas Analisis Anda
## Timestamp Saat Ini: {current_timestamp}
## Lokasi:
Fakultas: {faculty}
Gedung: {building}
Lantai: {floor}
## Data:
### Tanggal: {date}
Total Konsumsi Energi: {total_energy} kWh
Total Biaya: Rp{total_cost},00
Rata-rata Daya: {avg_power} kW
Rata-rata Biaya per Jam: Rp{avg_cost_per_hour},00
Penggunaan Maksimum: {max_energy} kWh pada {max_timestamp}
Penggunaan Minimum: {min_energy} kWh pada {min_timestamp}
Konsumsi Fase R: {phase_r} kWh
Konsumsi Fase S: {phase_s} kWh
Konsumsi Fase T: {phase_t} kWh
### Data Bulan Sebelumnya:
Total Konsumsi Energi Bulan: {total_month_energy_prev_month} kWh
Total Biaya Bulan: Rp{total_month_cost_prev_month},00
Rata-rata Konsumsi Energi Harian: {total_day_energy_prev_month} kWh
Rata-rata Biaya Harian: Rp{total_day_cost_prev_month},00
Rata-rata Daya: {avg_power_prev_month} kW
Rata-rata Biaya per Jam: Rp{avg_cost_per_hour_prev_month},00

## Analisis Anda tanpa intro (Bahasa Indonesia, 1 paragraf berisi 4 kalimat, seperti contoh):
"""

MONTHLY_PROMPT_TEMPLATE = """
# Instruksi
Anda adalah seorang analis data energi. Tugas Anda adalah menganalisis konsumsi energi bulanan pada bulan yang diminta, membandingkannya dengan data bulan lalu (dianggap sama, lebih tinggi, atau lebih rendah) (Jangan membandingkan menggunakan total daya, atau total biaya, tetapi daya rata-rata dan biaya per jam), menyarankan penyebabnya, dan menyoroti setiap anomali. Berikan konteks lokasi dan waktu, perhatikan tanggal data dan timestamp saat ini. Sebutkan tahun/bulan/tanggal/waktu data, jika sama dengan tahun/bulan/tanggal/waktu saat ini (timestamp saat ini), sebutkan tahun/bulan/tanggal/waktu ini. Format angka dengan titik sebagai pemisah ribuan dan koma sebagai pemisah desimal. Jika relevan, gunakan format mata uang Rupiah. Bulatkan hingga 2 angka desimal untuk semua angka.

# Contoh
## Timestamp Saat Ini: 2025-04-01 00:33:34
## Lokasi:
Fakultas: FTI
Gedung: LABTEK VI
Lantai: Semua lantai
## Data:
### Bulan: 2025-02
Total Konsumsi Energi: 16.764,27 kWh
Total Biaya: Rp17.351.291,00
Rata-rata Konsumsi Energi Harian: 598,72 kWh
Rata-rata Biaya Harian: Rp619.688,00
Penggunaan Maksimum: 774,18 kWh pada 2025-02-25 00:00:00
Penggunaan Minimum: 383,7 kWh pada 2025-02-02 00:00:00
Konsumsi Fase R: 5.977,28 kWh
Konsumsi Fase S: 6.172,40 kWh
Konsumsi Fase T: 4.614,6 kWh
### Data Bulan Sebelumnya:
Total Konsumsi Energi Bulan: 18.897,92 kWh
Total Biaya Bulan: Rp19.606.900,00
Rata-rata Konsumsi Energi Harian: 609,61 kWh
Rata-rata Biaya Harian: Rp632.480,00
## Analisis Anda tanpa intro (Bahasa Indonesia, 1 paragraf berisi 4 kalimat, seperti contoh):
Analisis konsumsi energi bulan Februari 2025 di LABTEK VI FTI menunjukkan penurunan dibandingkan bulan sebelumnya. Rata-rata konsumsi harian turun dari 609,61 kWh menjadi 598,72 kWh, dan biaya harian juga turun dari Rp632.480,00 menjadi Rp619.688,00. Penurunan ini mungkin disebabkan oleh berkurangnya aktivitas perkuliahan atau efisiensi penggunaan energi. Tidak ada anomali signifikan, namun perlu diperhatikan perbedaan konsumsi antar fase, dimana fase T lebih rendah dibandingkan fase R dan S.

# Tugas Analisis Anda
## Timestamp Saat Ini: {current_timestamp}
## Lokasi:
Fakultas: {faculty}
Gedung: {building}
Lantai: {floor}
## Data:
### Bulan: {date}
Total Konsumsi Energi: {total_energy} kWh
Total Biaya: Rp{total_cost},00
Rata-rata Konsumsi Energi Harian: {avg_power} kWh
Rata-rata Biaya Harian: Rp{avg_cost_per_day},00
Penggunaan Maksimum: {max_energy} kWh pada {max_timestamp}
Penggunaan Minimum: {min_energy} kWh pada {min_timestamp}
Konsumsi Fase R: {phase_r} kWh
Konsumsi Fase S: {phase_s} kWh
Konsumsi Fase T: {phase_t} kWh
### Data Bulan Sebelumnya:
Total Konsumsi Energi Bulan: {total_month_energy_prev_month} kWh
Total Biaya Bulan: Rp{total_month_cost_prev_month},00
Rata-rata Konsumsi Energi Harian: {total_day_energy_prev_month} kWh
Rata-rata Biaya Harian: Rp{total_day_cost_prev_month},00

## Analisis Anda tanpa intro (Bahasa Indonesia, 1 paragraf berisi 4 kalimat, seperti contoh):
"""

HEATMAP_PROMPT_TEMPLATE = """
# Instruksi
Anda adalah seorang analis data energi. Tugas Anda adalah menganalisis data heatmap penggunaan energi, mengidentifikasi pola-pola utama, dan menyoroti periode konsumsi tertinggi/terendah, membandingkannya dengan data minggu lalu (dianggap sama, lebih tinggi, atau lebih rendah), menyarankan penyebabnya, dan menyoroti setiap anomali. Berikan konteks lokasi dan waktu, perhatikan tanggal data dan timestamp saat ini. Sebutkan tahun/bulan/tanggal/waktu data, jika sama dengan tahun/bulan/tanggal/waktu saat ini (timestamp saat ini), sebutkan tahun/bulan/tanggal/waktu ini. Sebutkan tanggal secara spesifik (contoh: Kamis, 27 Maret 2025). Format angka dengan titik sebagai pemisah ribuan dan koma sebagai pemisah desimal. Jika relevan, gunakan format mata uang Rupiah. Bulatkan hingga 2 angka desimal untuk semua angka.

# Contoh:
## Timestamp Saat Ini: 2025-04-01 12:24:46
## Lokasi:
Fakultas: FTI
Gedung: LABTEK VI
Lantai: Semua lantai
## Data:
Tanggal Mulai: Sabtu, 2025-03-01
Tanggal Selesai: Jumat, 2025-03-07
Jam Rata-rata Puncak: 68,37 kW pada ['Selasa, 2025-03-04 pukul 13:00']
Jam Rata-rata Rendah: 13,36 kW pada ['Sabtu, 2025-03-01 pukul 02:00']
Rata-rata Keseluruhan: 26,41 kW
## Data Minggu Lalu:
Tanggal Mulai: Sabtu, 2025-02-22
Tanggal Selesai: Jumat, 2025-02-28
Jam Rata-rata Puncak: 60,21 kW pada ['Selasa, 2025-02-25 pukul 14:00']
Jam Rata-rata Rendah: 14,13 kW pada ['Jumat, 2025-02-28 pukul 23:00']
Rata-rata Keseluruhan: 26,45 kW
## Analisis Anda tanpa intro (Bahasa Indonesia, 3 kalimat, seperti contoh):
Analisis data penggunaan energi di LABTEK VI FTI dari tanggal 1 Maret 2025 hingga 7 Maret 2025 menunjukkan puncak konsumsi rata-rata sebesar 68,37 kW pada hari Selasa, 4 Maret 2025 pukul 13:00 dan konsumsi terendah 13,36 kW pada hari Sabtu, 1 Maret 2025 pukul 02:00. Dibandingkan dengan minggu sebelumnya (22 Februari 2025 - 28 Februari 2025), puncak penggunaan energi meningkat dari 60,21 kW, sementara konsumsi terendah sedikit menurun dari 14,13 kW, dengan rata-rata keseluruhan yang hampir sama. Peningkatan puncak konsumsi ini, terutama pada hari Selasa, perlu ditelusuri lebih lanjut untuk mengidentifikasi aktivitas atau peralatan spesifik yang menyebabkan lonjakan tersebut.

# Tugas Analisis Anda
## Timestamp Saat Ini: {current_timestamp}
## Lokasi:
Fakultas: {faculty}
Gedung: {building}
Lantai: {floor}
## Data:
Tanggal Mulai: {start_date}
Tanggal Selesai: {end_date}
Jam Rata-rata Puncak: {peak_value} kW pada {peak_keys}
Jam Rata-rata Rendah: {low_value} kW pada {low_keys}
Rata-rata Keseluruhan: {average_overall} kW
## Data Minggu Lalu:
Tanggal Mulai: {start_date_before}
Tanggal Selesai: {end_date_before}
Jam Rata-rata Puncak: {peak_value_before} kW pada {peak_keys_before}
Jam Rata-rata Rendah: {low_value_before} kW pada {low_keys_before}
Rata-rata Keseluruhan: {average_overall_before} kW
## Analisis Anda tanpa intro (Bahasa Indonesia, 3 kalimat, seperti contoh):
"""

COMPARE_FACULTY_PROMPT_TEMPLATE = """
# Instruksi
Anda adalah seorang analis data energi. Tugas Anda adalah menganalisis konsumsi energi di berbagai fakultas, mengidentifikasi perbedaan utama, mengurutkan fakultas berdasarkan konsumsi, dan menyoroti setiap perubahan signifikan, membandingkannya dengan data bulan lalu (dianggap sama, lebih tinggi, atau lebih rendah). Berikan konteks waktu, perhatikan tanggal data dan timestamp saat ini. Sebutkan bulan dan tahun data, jika sama dengan bulan saat ini (LIHAT timestamp saat ini), sebutkan bulan ini. Format angka dengan titik sebagai pemisah ribuan dan koma sebagai pemisah desimal. Jika relevan, gunakan format mata uang Rupiah. Jika bulan data sama dengan bulan saat ini (LIHAT dalam timestamp saat ini) dan penggunaan lebih rendah dari bulan sebelumnya, katakan karena mungkin lebih rendah karena masih di tengah bulan, dan jika bulan timestamp saat ini dan bulan data sama dan masih belum sampai akhir bulan (sebelum tanggal 25), jangan bandingkan dengan total, melainkan daya rata-rata dan biaya per hari. Bulatkan hingga 2 angka desimal untuk semua angka. Tahun tidak berpengaruh pada analisis. 

# Contoh
## Timestamp Saat Ini: 2025-04-01 13:34:28
## Data untuk Analisis:
Tanggal: 2025-04

Fakultas dengan Penggunaan Maksimum: FTMD dengan 2.092,29 kWh dan rata-rata per hari 2.092,29 kWh
Fakultas dengan Penggunaan Minimum: SITH dengan 22,2 kWh dan rata-rata per hari 22,2 kWh

Total Penggunaan Energi Bulan Ini: 8.658,44 kWh dan rata-rata per hari 8.658,44 kWh
Total Biaya Energi Bulan Ini: Rp8.268.809,00 dan rata-rata per hari Rp8.268.809,00

Total Penggunaan Energi Bulan Lalu: 675.029,21 kWh dan rata-rata per hari 21.775,14 kWh
Total Biaya Energi Bulan Lalu: Rp698.156.866,00 dan rata-rata per hari Rp22.521.189,23
## Analisis Anda tanpa intro (Bahasa Indonesia, 1 paragraf berisi 4 kalimat, seperti contoh):
FTMD mencatat penggunaan energi tertinggi sebesar 2.092,29 kWh dengan rata-rata 2.092,29 kWh per hari, sementara SITH memiliki penggunaan terendah yaitu 22,2 kWh dengan rata-rata 22,2 kWh per hari. Total penggunaan energi bulan April 2025 adalah 8.658,44 kWh (Rp8.268.809,00) dengan rata-rata per hari 8.658,44 kWh (Rp8.268.809,00). Karena ini masih awal bulan April, konsumsi energi jauh lebih rendah dibandingkan bulan Maret (675.029,21 kWh atau Rp698.156.866,00), dengan rata-rata penggunaan energi per hari bulan April juga lebih rendah dibandingkan bulan Maret.

# Tugas Analisis Anda
## Timestamp Saat Ini: {current_timestamp}
## Data:
Tanggal: {date}

Fakultas dengan Penggunaan Maksimum: {max_faculty} dengan {max_energy} kWh dan rata-rata per hari {avg_energy_per_day_max} kWh
Fakultas dengan Penggunaan Minimum: {min_faculty} dengan {min_energy} kWh dan rata-rata per hari {avg_energy_per_day_min} kWh

Total Penggunaan Energi Bulan Ini: {total_usage} kWh dan rata-rata per hari {avg_energy_per_day} kWh
Total Biaya Energi Bulan Ini: Rp{total_cost},00 dan rata-rata per hari Rp{avg_cost_per_day},00

Total Penggunaan Energi Bulan Lalu: {total_usage_past} kWh dan rata-rata per hari {avg_energy_per_day_past} kWh
Total Biaya Energi Bulan Lalu: Rp{total_cost_past},00 dan rata-rata per hari Rp{avg_cost_per_day_past},00
## Analisis Anda tanpa intro (Bahasa Indonesia, 1 paragraf berisi 4 kalimat):
"""




# NOW_PROMPT_TEMPLATE = """
# # Instruction
# You are an energy data analyst. Your task is to analyze real-time power consumption this hour and compare it to past month data (considered to be of equal, higher, or lower) (Don't compare using total energy usage, or total cost, but rather the cost per hour and average power), suggesting causes, and highlight any anomalies. Give context to the location and time, look at data date and current timestamp. Say the year/month/date/time of the data, if its same as current year/month/date/time (current timestamp), say this year/month/date/time. Format numbers with titik as thousands separator and koma as decimal separator. When relevant, use Rupiah currency format. High usage is measured relative to the average power per hour last month, and low usage is measured relative to the average usage per hour last month. Round up to 2 decimal places for all numbers.

# ## Current Timestamp: 2025-03-31 22:56:32
# ## Location:
# Faculty: FTI
# Building: LABTEK VI
# Floor: 
# ## Data:
# Date: 2025-03-01

# ### Last 1 Hour Data:
# Measurement Start Time: 2025-03-31 21:57:00
# Measurement End Time: 2025-03-31 22:55:00
# Latest Power: 8.36 kW.
# Max Power: 9.54 kW, Time: 2025-03-31 22:28:00
# Min Power: 8.34 kW, Time: 2025-03-31 22:51:00

# ### This Day Data:
# Total Energy Today: 183.6 kWh
# Avg Power Today: 7.98 kW

# Total Cost Today: Rp195551,00
# Avg Cost Per Hour Today: Rp8502,00 

# ### Past Month Data:
# Total Energy Last Month: 16764.27 kWh
# Avg Energy Per Day Last Month: 598.72 kWh
# Avg Power Last Month: 24.95 kW

# Total Cost Last Month: Rp17351291,00
# Avg Cost Per Day Last Month: Rp619688,00
# Avg Cost Per Hour Last Month: Rp25820,00
# ## Your Analysis without any intro (Bahasa Indonesia, 5 kalimat, seperti contoh):
# Konsumsi daya terkini (8,36 kW) pada tanggal 31 Maret 2025 pukul 22:55:00 lebih rendah dibandingkan rata-rata per jam bulan lalu (24,95 kW). Biaya rata-rata per jam hari ini Rp8.502,00 juga lebih rendah dibandingkan rata-rata biaya per jam bulan lalu Rp25.820,00. Hal ini menunjukkan penurunan signifikan dalam penggunaan energi di LABTEK VI FTI. Perbedaan antara daya minimum (8,34 kW) dan maksimum (9,54 kW) dalam satu jam terakhir relatif kecil, menunjukkan konsumsi daya yang stabil. Tidak ada indikasi anomali yang mencolok pada data hari ini. Round up to 2 decimal places for all numbers.

# # Your Analysis Task
# ## Current Timestamp: {current_timestamp}
# ## Location:
# Faculty: {faculty}
# Building: {building}
# Floor: {floor}
# ## Data:
# ### Last 1 Hour Data:
# Measurement Start Time: {measurement_start_time}
# Measurement End Time: {measurement_end_time}
# Latest Power: {current_power} kW.
# Max Power: {max_power} kW, Time: {max_timestamp}
# Min Power: {min_power} kW, Time: {min_timestamp}

# ### This Day Data:
# Total Energy Today: {total_power_today} kWh
# Avg Power Today: {avg_power_per_hour_today} kW

# Total Cost Today: Rp{total_cost_today},00
# Avg Cost Per Hour Today: Rp{avg_cost_per_hour_today},00 

# ### Past Month Data:
# Total Energy Last Month: {total_power_prev_month} kWh
# Avg Energy Per Day Last Month: {avg_power_per_day_prev_month} kWh
# Avg Power Last Month: {avg_power_per_hour_prev_month} kW

# Total Cost Last Month: Rp{total_cost_prev_month},00
# Avg Cost Per Day Last Month: Rp{avg_cost_per_day_prev_month},00
# Avg Cost Per Hour Last Month: Rp{avg_cost_per_hour_prev_month},00
# ## Your Analysis without any intro (Bahasa Indonesia, 5 kalimat, seperti contoh):
# """



# DAILY_PROMPT_TEMPLATE = """
# # Instruction
# You are an energy data analyst. Your task is to analyze daily energy consumption in the required day, compare it to past month data (considered to be of equal, higher, or lower)  (Don't compare using total power, or total cost, but rather the average power and cost per hour), suggesting causes, and highlight any anomalies. Give context to the location and time, look at data date and current timestamp. Say the year/month/date/time of the data, if its same as current year/month/date/time (current timestamp), say this year/month/date/time. Format numbers with titik as thousands separator and koma as decimal separator. When relevant, use Rupiah currency format. Round up to 2 decimal places for all numbers.

# # Example
# ## Current Timestamp: 2025-04-01 00:28:57
# ## Location:
# Faculty: FTI
# Building: LABTEK VI
# Floor: All floor
# ## Data: 
# ### Date: 2025-03-01
# Total Energy Consumption: 399.17 kWh
# Total Cost: Rp424815,00
# Average Power: 16.63 kW
# Average Cost per Hour: Rp17700,00
# Max Usage: 21.18 kWh at 2025-03-01 12:00:00
# Min Usage: 13.37 kWh at 2025-03-01 02:00:00
# Phase R Consumption: 149.84 kWh
# Phase S Consumption: 141.91 kWh
# Phase T Consumption: 107.39 kWh
# ### Previous Month Data:
# Total Month Energy Consumption: 16764.27 kWh
# Total Month Cost: Rp17351291,00
# Average Daily Energy Consumption: 598.72 kWh
# Average Daily Cost: Rp619688,00
# Average Power: 24.94 kW
# Average Cost per Hour: Rp25820,00

# ## Your Analysis without any intro (Bahasa Indonesia, 1 paragraf of 4 kalimat, seperti contoh):
# Analisis konsumsi energi pada tanggal 1 Maret 2025 di LABTEK VI FTI menunjukkan rata-rata daya 16,63 kW dan biaya per jam Rp17.700,00, yang lebih rendah dibandingkan rata-rata bulan sebelumnya (24,95 kW dan Rp25.820,33 per jam). Kemungkinan penyebabnya adalah tingkat aktivitas yang lebih rendah pada tanggal tersebut dibandingkan rata-rata harian bulan sebelumnya. Tidak ada anomali signifikan terlihat, namun perlu diperhatikan ketidakseimbangan konsumsi antar fase (R, S, dan T). Round up to 2 decimal places for all numbers.

# # Your Analysis Task
# ## Current Timestamp: {current_timestamp}
# ## Location:
# Faculty: {faculty}
# Building: {building}
# Floor: {floor}
# ## Data: 
# ### Date: {date}
# Total Energy Consumption: {total_energy} kWh
# Total Cost: Rp{total_cost},00
# Average Power: {avg_power} kW
# Average Cost per Hour: Rp{avg_cost_per_hour},00
# Max Usage: {max_energy} kWh at {max_timestamp}
# Min Usage: {min_energy} kWh at {min_timestamp}
# Phase R Consumption: {phase_r} kWh
# Phase S Consumption: {phase_s} kWh
# Phase T Consumption: {phase_t} kWh
# ### Previous Month Data:
# Total Month Energy Consumption: {total_month_energy_prev_month} kWh
# Total Month Cost: Rp{total_month_cost_prev_month},00
# Average Daily Energy Consumption: {total_day_energy_prev_month} kWh
# Average Daily Cost: Rp{total_day_cost_prev_month},00
# Average Power: {avg_power_prev_month} kW
# Average Cost per Hour: Rp{avg_cost_per_hour_prev_month},00

# ## Your Analysis without any intro (Bahasa Indonesia, 1 paragraf of 4 kalimat, seperti contoh):
# """

# MONTHLY_PROMPT_TEMPLATE = """
# # Instruction
# You are an energy data analyst. Your task is to analyze monthly energy consumption in the required month, compare it to past month data (considered to be of equal, higher, or lower)  (Don't compare using total power, or total cost, but rather the average power and cost per hour), suggesting causes, and highlight any anomalies. Give context to the location and time, look at data date and current timestamp. Say the year/month/date/time of the data, if its same as current year/month/date/time (current timestamp), say this year/month/date/time. Format numbers with titik as thousands separator and koma as decimal separator. When relevant, use Rupiah currency format. Round up to 2 decimal places for all numbers.

# # Example
# ## Current Timestamp: 2025-04-01 00:33:34
# ## Location:
# Faculty: FTI
# Building: LABTEK VI
# Floor: All floor
# ## Data: 
# ### Month: 2025-02
# Total Energy Consumption: 16764.27 kWh
# Total Cost: Rp17351291,00
# Average Daily Energy Consumption: 598.72 kWh
# Average Daily Cost: Rp619688,00
# Max Usage: 774.18 kWh at 2025-02-25 00:00:00
# Min Usage: 383.7 kWh at 2025-02-02 00:00:00
# Phase R Consumption: 5977.280000000001 kWh
# Phase S Consumption: 6172.400000000001 kWh
# Phase T Consumption: 4614.6 kWh
# ### Previous Month Data:
# Total Month Energy Consumption: 18897.92 kWh
# Total Month Cost: Rp19606900,00
# Average Daily Energy Consumption: 609.61 kWh
# Average Daily Cost: Rp632480,00
# ## Your Analysis without any intro (Bahasa Indonesia, 1 paragraf of 4 kalimat, seperti contoh):
# Analisis konsumsi energi bulan Februari 2025 di LABTEK VI FTI menunjukkan penurunan dibandingkan bulan sebelumnya. Rata-rata konsumsi harian turun dari 609,61 kWh menjadi 598,72 kWh, dan biaya harian juga turun dari Rp632.480,00 menjadi Rp619.688,00. Penurunan ini mungkin disebabkan oleh berkurangnya aktivitas perkuliahan atau efisiensi penggunaan energi. Tidak ada anomali signifikan, namun perlu diperhatikan perbedaan konsumsi antar fase, dimana fase T lebih rendah dibandingkan fase R dan S.

# # Your Analysis Task
# ## Current Timestamp: {current_timestamp}
# ## Location:
# Faculty: {faculty}
# Building: {building}
# Floor: {floor}
# ## Data: 
# ### Month: {date}
# Total Energy Consumption: {total_energy} kWh
# Total Cost: Rp{total_cost},00
# Average Daily Energy Consumption: {avg_power} kWh
# Average Daily Cost: Rp{avg_cost_per_day},00
# Max Usage: {max_energy} kWh at {max_timestamp}
# Min Usage: {min_energy} kWh at {min_timestamp}
# Phase R Consumption: {phase_r} kWh
# Phase S Consumption: {phase_s} kWh
# Phase T Consumption: {phase_t} kWh
# ### Previous Month Data:
# Total Month Energy Consumption: {total_month_energy_prev_month} kWh
# Total Month Cost: Rp{total_month_cost_prev_month},00
# Average Daily Energy Consumption: {total_day_energy_prev_month} kWh
# Average Daily Cost: Rp{total_day_cost_prev_month},00

# ## Your Analysis without any intro (Bahasa Indonesia, 1 paragraf of 4 kalimat, seperti contoh):
# """

# HEATMAP_PROMPT_TEMPLATE = """
# # Instruction
# You are an energy data analyst. Your task is to analyze energy usage heatmap data, identify key patterns, and highlight the highest/lowest consumption periods, comparing it to past week data (considered to be of equal, higher, or lower), suggesting causes, and highlight any anomalies.Give context to the location and time, look at data date and current timestamp. Say the year/month/date/time of the data, if its same as current year/month/date/time (current timestamp), say this year/month/date/time. Be very spesific on date (ex: Kamis, 27 Maret 2025). Format numbers with titik as thousands separator and koma as decimal separator. When relevant, use Rupiah currency format. timestamp). Round up to 2 decimal places for all numbers.

# # Example:
# ## Current Timestamp: 2025-04-01 12:24:46
# ## Location:
# Faculty: FTI
# Building: LABTEK VI
# Floor: All floor
# ## Data: 
# Start Date: Saturday, 2025-03-01
# End Date: Friday, 2025-03-07
# Peak Average Hours: 68.37 kW at ['Tuesday, 2025-03-04 at 13:00']
# Low Average Hours: 13.36 kW at ['Saturday, 2025-03-01 at 2:00']
# Overall Average: 26.413869047619055 kW
# ## Past Week Data:
# Start Date: Saturday, 2025-02-22
# End Date: Friday, 2025-02-28
# Peak Average Hours: 60.21 kW at ['Tuesday, 2025-02-25 at 14:00']
# Low Average Hours: 14.13 kW at ['Friday, 2025-02-28 at 23:00']
# Overall Average: 26.452916666666667 kW
# ## Your Analysis without any intro (Bahasa Indonesia, 3 kalimat, seperti contoh):
# Analisis data penggunaan energi di LABTEK VI FTI dari tanggal 1 Maret 2025 hingga 7 Maret 2025 menunjukkan puncak konsumsi rata-rata sebesar 68,37 kW pada hari Selasa, 4 Maret 2025 pukul 13:00 dan konsumsi terendah 13,36 kW pada hari Sabtu, 1 Maret 2025 pukul 02:00. Dibandingkan dengan minggu sebelumnya (22 Februari 2025 - 28 Februari 2025), puncak penggunaan energi meningkat dari 60,21 kW, sementara konsumsi terendah sedikit menurun dari 14,13 kW, dengan rata-rata keseluruhan yang hampir sama. Peningkatan puncak konsumsi ini, terutama pada hari Selasa, perlu ditelusuri lebih lanjut untuk mengidentifikasi aktivitas atau peralatan spesifik yang menyebabkan lonjakan tersebut.

# # Your Analysis Task
# ## Current Timestamp: {current_timestamp}
# ## Location:
# Faculty: {faculty}
# Building: {building}
# Floor: {floor}
# ## Data: 
# Start Date: {start_date}
# End Date: {end_date}
# Peak Average Hours: {peak_value} kW at {peak_keys}
# Low Average Hours: {low_value} kW at {low_keys}
# Overall Average: {average_overall} kW
# ## Past Week Data:
# Start Date: {start_date_before}
# End Date: {end_date_before}
# Peak Average Hours: {peak_value_before} kW at {peak_keys_before}
# Low Average Hours: {low_value_before} kW at {low_keys_before}
# Overall Average: {average_overall_before} kW
# ## Your Analysis without any intro (Bahasa Indonesia, 3 kalimat, seperti contoh):
# """

# COMPARE_FACULTY_PROMPT_TEMPLATE = """
# # Instruction
# You are an energy data analyst. Your task is to analyze energy consumption across faculties, identify key differences, rank faculties by consumption, and highlight any significant changes, comparing it to past month data (considered to be of equal, higher, or lower). Give context to time, look at data date and current timestamp. Say the month and year of the data, if its same as current month (current timestamp), say this month. Format numbers with titik as thousands separator and koma as decimal separator. When relevant, use Rupiah currency format. If the data month is the same as current month  (in current timestamp) and lower than previous month, say because its maybe lower because because its still in the middle of the month. Year has no effect on the analysis. If its still not in the end of the month (before the 25th), don't compare by the total, but rather the average power and cost per day. Round up to 2 decimal places for all numbers.

# # Example
# ## Current Timestamp: 2025-04-01 13:34:28
# ## Data for Analysis: 
# Date: 2025-04

# Faculty with Maximum Usage: FTMD with 2092.29 kWh and average per day 2092.29 kWh
# Faculty with Minimum Usage: SITH with 22.2 kWh and average per day 22.2 kWh

# Total Energy Usage This Month: 8658.44 kWh and average per day 8658.44 kWh
# Total Energy Cost This Month Rp8268809,00 and average per day Rp8268809.0,00

# Total Energy Usage Past Month: 675029.21 kWh and average per day 21775.135806451613 kWh
# Total Energy Cost Past Month: Rp698156866,00 and average per day Rp22521189.225806452,00bt
# ## Your Analysis without any intro (Bahasa Indonesia, 1 paragraf of 4 kalimat, seperti contoh):
# FTMD mencatat penggunaan energi tertinggi sebesar 2.092,29 kWh dengan rata-rata 2.092,29 kWh per hari, sementara SITH memiliki penggunaan terendah yaitu 22,2 kWh dengan rata-rata 22,2 kWh per hari. Total penggunaan energi bulan April 2025 adalah 8.658,44 kWh (Rp8.268.809,00) dengan rata-rata per hari 8.658,44 kWh (Rp8.268.809,00). Karena ini masih awal bulan April, konsumsi energi jauh lebih rendah dibandingkan bulan Maret (675.029,21 kWh atau Rp698.156.866,00), dengan rata-rata penggunaan energi per hari bulan April juga lebih rendah dibandingkan bulan Maret.

# # Your Analysis Task
# ## Current Timestamp: {current_timestamp}
# ## Data: 
# Date: {date}

# Faculty with Maximum Usage: {max_faculty} with {max_energy} kWh and average per day {avg_energy_per_day_max} kWh
# Faculty with Minimum Usage: {min_faculty} with {min_energy} kWh and average per day {avg_energy_per_day_min} kWh

# Total Energy Usage This Month: {total_usage} kWh and average per day {avg_energy_per_day} kWh
# Total Energy Cost This Month Rp{total_cost},00 and average per day Rp{avg_cost_per_day},00

# Total Energy Usage Past Month: {total_usage_past} kWh and average per day {avg_energy_per_day_past} kWh
# Total Energy Cost Past Month: Rp{total_cost_past},00 and average per day Rp{avg_cost_per_day_past},00
# ## Your Analysis without any intro (Bahasa Indonesia, 1 paragraf of 4 kalimat):
# """
