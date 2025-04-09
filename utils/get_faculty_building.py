import asyncio
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


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


async def main():
    """
    Fetches all faculties and their buildings and prints them in a formatted
    string.
    """
    try:
        faculties_data = await async_fetch_fakultas()
        if faculties_data and "fakultas" in faculties_data:
            faculties = faculties_data["fakultas"]
            output_string = "Faculty List:\n"
            for i, faculty in enumerate(faculties):
                faculty_label = faculty["label"]
                faculty_value = faculty["value"]
                print(f"Fetching buildings for faculty: {faculty_label} ({faculty_value})")
                output_string += f"{i + 1}. {faculty_label}:\n"
                output_string += "Building List:\n"

                try:
                    buildings_data = await async_fetch_gedung(faculty_value)
                    if buildings_data and "gedung" in buildings_data:
                        buildings = buildings_data["gedung"]
                        for building in buildings:
                            building_label = building["label"]
                            output_string += f"- {building_label}\n"
                    else:
                        output_string += "- No buildings found for this faculty.\n"
                except Exception as e:
                    output_string += (
                        f"- Error fetching buildings: {e}\n"
                    )  # Handle errors fetching buildings
            print(output_string)
        else:
            print("No faculties data found.")
    except Exception as e:
        print(f"Error fetching faculties: {e}")  # Handle errors fetching faculties


if __name__ == "__main__":
    asyncio.run(main())
