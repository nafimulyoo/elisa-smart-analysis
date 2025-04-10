import requests
import time
import psutil

ENDPOINT = "http://localhost:8000/api/web?prompt=berapa pemakaian ftmd bulan lalu"
# ENDPOINT = "http://localhost:8000/test"
REQUESTS = 1000000  # Adjust based on your needs

initial_memory = psutil.virtual_memory()

for i in range(REQUESTS):
    time.sleep(1)
    print(f"Before {i+1}:" + str(psutil.virtual_memory()))
    response = requests.get(ENDPOINT)
    assert response.status_code == 200
    if i % 1 == 0:
        print(f"After {i+1}:" + str(psutil.virtual_memory()))

print(f"Initial memory: {initial_memory}")
print(f"Final memory: {psutil.virtual_memory()}")