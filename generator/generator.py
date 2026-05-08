import requests
import random
import time
from datetime import datetime

URL = "http://localhost:5000/meter-data"

# ---------------- BASELINE USAGE ---------------- #

BASE_USAGE = {
    1: 3.5,
    2: 4.0,
    3: 2.8,
    4: 3.2,
    5: 4.5
}

# ---------------- LIVE LOOP ---------------- #

while True:

    house_id = random.randint(1, 5)

    baseline = BASE_USAGE[house_id]

    # Smooth realistic fluctuation
    usage = baseline + random.uniform(-0.5, 0.5)

    # Rare anomaly injection
    anomaly_chance = random.randint(1, 20)

    if anomaly_chance == 1:
        usage = random.uniform(0.1, 0.8)

    # Prevent negative values
    usage = round(max(0.1, usage), 2)

    data = {
        "house_id": house_id,
        "usage": usage,
        "timestamp": str(datetime.now())
    }

    try:

        response = requests.post(
            URL,
            json=data
        )

        print(
            f"Sent: {data} | "
            f"Status: {response.json()['status']} | "
            f"Score: {response.json()['anomaly_score']}"
        )

    except Exception as e:

        print("Error:", e)

    time.sleep(3)