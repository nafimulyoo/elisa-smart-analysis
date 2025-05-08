import requests
import csv
import time

random_dates = [
    "2024-03-15",
    "2025-01-20",
    "2025-01-05",
    "2024-12-01",
    "2024-09-28",
    "2025-05-01",
    "2024-06-12",
    "2025-04-18",
    "2024-10-03",
    "2024-01-23",
    "2024-11-08",
    "2024-08-29",
    "2025-02-14",
    "2024-06-07",
    "2024-04-05",
    "2024-12-20",
    "2024-09-16",
    "2025-03-02",
    "2024-11-25",
    "2024-07-31",
]
random_months = [
    "2024-03",
    "2025-01",
    "2025-01",
    "2024-12",
    "2024-09",
    "2025-05",
    "2024-06",
    "2025-04",
    "2024-10",
    "2024-01",
    "2024-11",
    "2024-08",
    "2025-02",
    "2024-06",
    "2024-04",
    "2024-12",
    "2024-09",
    "2025-03",
    "2024-11",
    "2024-07",
]
random_faculty_and_building_pair = [
    ["FTI", "LABTEK VI", ""],
    ["UNIT KERJA", "Villa Merah", ""],
    ["FTTM", "Gedung Energi", ""],
    ["", "", ""],
    
    ["SBM", "", ""],
    ["FSRD", "", ""],
    ["FTI", "LABTEK VI", ""],
    ["FSRD", "CAD", ""],
    ["SBM", "SBM FREEPORT", ""],
    ["FTI", "", ""],
    ["UNIT KERJA", "Villa Merah", ""],
    ["SITH", "LABTEK XI", ""],
    ["FTMD", "", ""],
    ["STEI", "Lab. Konversi", ""],
    ["", "", ""],
    ["", "LABTEK X", ""],
    ["FTTM", "Gedung Energi", ""],
    ["FTI", "LABTEK VI", "Lab Manajemen Energi"],
    ["", "", ""],
    ["FMIPA", "FISIKA", ""],
]


def get_response(url, max_retries=3, retry_delay=1):
    """
    Simulates a GET request to the API with retry logic.

    Args:
        url (str): The URL to request.
        max_retries (int): Maximum number of retries.
        retry_delay (int): Delay in seconds between retries.

    Returns:
        requests.Response: The response object, or None if all retries fail.
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(f"http://0.0.0.0:8080{url}")
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response  # Return response if successful
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)  # Wait before retrying
            else:
                print(f"Max retries reached. Unable to get response from {url}")
                return None  # Return None if all retries failed




def process_and_write_data(
    file_prefix, data_type, dates, faculty_building_data=None, model=""
):
    """
    Processes data and writes to a CSV file with retry logic for empty analyses.

    Args:
        file_prefix (str): Prefix for the CSV filename.
        data_type (str): Type of data ('daily', 'monthly', 'faculty', 'heatmap').
        dates (list): List of dates.
        faculty_building_data (list, optional): List of faculty/building pairs.
    """
    filename = f"{model}_analysis_{file_prefix}.csv"
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)

        # Write the header row
        if data_type in ("daily", "monthly", "heatmap"):
            writer.writerow(
                ["Date", "Faculty", "Building", "Floor", "Analysis", "Time (s)"]
            )
        elif data_type == "faculty":
            writer.writerow(["Date", "Analysis", "Time (s)"])

        for i in range(case_count):
            date = dates[i]
            faculty = (
                faculty_building_data[i][0] if faculty_building_data else None
            )
            building = (
                faculty_building_data[i][1] if faculty_building_data else None
            )
            floor = (
                faculty_building_data[i][2] if faculty_building_data else None
            )

            if data_type == "now":
                url = f"/api/analysis/now?faculty={faculty}&building={building}&floor={floor}&model={model}"
            elif data_type == "daily":
                url = f"/api/analysis/daily?date={date}&faculty={faculty}&building={building}&floor={floor}&model={model}"
            elif data_type == "monthly":
                url = f"/api/analysis/monthly?date={date}&faculty={faculty}&building={building}&floor={floor}&model={model}"
            elif data_type == "faculty":
                url = f"/api/analysis/faculty?date={date}&model={model}"
            elif data_type == "heatmap":
                start_date = date + "-01"
                end_date = date + "-07"
                url = f"/api/analysis/heatmap?start={start_date}&end={end_date}&faculty={faculty}&building={building}&floor={floor}&model={model}"

            analysis = ""
            max_attempts = 10  # Maximum attempts to get non-empty analysis
            attempt = 0
            start_time = time.time()

            while not analysis and attempt < max_attempts:
                response = get_response(url)
                if response:
                    response_json = response.json()
                    analysis = response_json.get("analysis", "")
                else:
                    analysis = ""  # Ensure analysis is empty if response is None

                if not analysis:
                    attempt += 1
                    print(
                        f"Attempt {attempt}: Empty analysis for {date}. Retrying..."
                    )
                    time.sleep(2)  # Wait before retrying
                else:
                    print(f"Analysis found on attempt {attempt + 1}")

            end_time = time.time()
            elapsed_time = end_time - start_time

            # Print to console
            print(f"Case {date} - {faculty} - {building} - {floor}:")
            print(f" Analysis: {analysis}")
            print(f" Time: {elapsed_time:.4f} seconds")

            # Write to CSV
            if data_type in ("daily", "monthly", "heatmap"):
                writer.writerow(
                    [date, faculty, building, floor, analysis, elapsed_time]
                )
            elif data_type == "faculty":
                writer.writerow([date, analysis, elapsed_time])



models = ["gemini", "gemma", "deepseek"]
case_count = 4

# for model in models:
#     #  NOW
#     process_and_write_data(
#         "now", "now", random_dates, random_faculty_and_building_pair, model
#     )

# # DAILY
# process_and_write_data(
#     "daily", "daily", random_dates, random_faculty_and_building_pair
# )

# # MONTHLY
# process_and_write_data(
#     "monthly", "monthly", random_months, random_faculty_and_building_pair
# )

# # FACULTY
# process_and_write_data("compare", "faculty", random_months)

# # HEATMAP
# process_and_write_data(
#     "heatmap", "heatmap", random_months, random_faculty_and_building_pair
# )

# DAILY

print("Daily Analysis URLs:")
for i in range(20):
    building = random_faculty_and_building_pair[i][1]
    faculty = random_faculty_and_building_pair[i][0]
    floor = random_faculty_and_building_pair[i][2]
    date = random_dates[i]

    # change space to %20
    building = building.replace(" ", "%20")
    faculty = faculty.replace(" ", "%20")
    floor = floor.replace(" ", "%20")

    print(f"Faculty: {faculty}, Building: {building}, Floor: {floor}, Date: {date} => http://localhost:3000/daily?date={date}&faculty={faculty}&building={building}&floor={floor}")

# MONTHLY
print("\nMonthly Analysis URLs:")
for i in range(20):
    building = random_faculty_and_building_pair[i][1]
    faculty = random_faculty_and_building_pair[i][0]
    floor = random_faculty_and_building_pair[i][2]
    date = random_months[i]

    # change space to %20
    building = building.replace(" ", "%20")
    faculty = faculty.replace(" ", "%20")
    floor = floor.replace(" ", "%20")

    print(f"Faculty: {faculty}, Building: {building}, Floor: {floor}, Date: {date} => http://localhost:3000/monthly?date={date}&faculty={faculty}&building={building}&floor={floor}")

# FACULTY
print("\nFaculty Analysis URLs:")
for i in range(20):
    date = random_months[i]
    print(f"Date: {date} => http://localhost:3000/faculty?date={date}")

# HEATMAP
print("\nHeatmap Analysis URLs:")
for i in range(20):
    building = random_faculty_and_building_pair[i][1]
    faculty = random_faculty_and_building_pair[i][0]
    floor = random_faculty_and_building_pair[i][2]
    start_date = random_months[i] + "-01"
    end_date = random_months[i] + "-07"

    # change space to %20
    building = building.replace(" ", "%20")
    faculty = faculty.replace(" ", "%20")
    floor = floor.replace(" ", "%20")

    print(f"Faculty: {faculty}, Building: {building}, Floor: {floor}, Date: {date} => http://localhost:3000/heatmap?start={start_date}&end={end_date}&faculty={faculty}&building={building}&floor={floor}")