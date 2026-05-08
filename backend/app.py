from flask import Flask, request, jsonify, Response
from prometheus_client import Counter, Gauge, generate_latest
import csv
import os

app = Flask(__name__)

CSV_FILE = "data.csv"

# ---------------- HOUSE BASELINES ---------------- #

BASELINE_USAGE = {
    1: 3.5,
    2: 4.0,
    3: 2.8,
    4: 3.2,
    5: 4.5
}

# ---------------- METRICS ---------------- #

REQUEST_COUNT = Counter(
    "meter_requests_total",
    "Total meter requests"
)

SUSPICIOUS_COUNT = Counter(
    "suspicious_events_total",
    "Total suspicious events"
)

CURRENT_USAGE = Gauge(
    "current_power_usage",
    "Current power usage",
    ["house_id"]
)

ANOMALY_SCORE = Gauge(
    "anomaly_score",
    "Calculated anomaly score",
    ["house_id"]
)

# ---------------- CSV SETUP ---------------- #

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "house_id",
            "usage",
            "timestamp",
            "status",
            "baseline",
            "anomaly_score",
            "severity"
        ])

# ---------------- ROUTES ---------------- #

@app.route("/meter-data", methods=["POST"])
def meter_data():

    data = request.json

    house_id = int(data["house_id"])
    usage = float(data["usage"])
    timestamp = data["timestamp"]

    REQUEST_COUNT.inc()

    CURRENT_USAGE.labels(
        house_id=str(house_id)
    ).set(usage)

    baseline = BASELINE_USAGE.get(house_id, 3.0)

    deviation_percent = abs(
        (baseline - usage) / baseline
    ) * 100

    anomaly_score = round(deviation_percent, 2)

    ANOMALY_SCORE.labels(
        house_id=str(house_id)
    ).set(anomaly_score)

    status = "NORMAL"
    severity = "LOW"

    # ---------------- DETECTION LOGIC ---------------- #

    if anomaly_score > 70:
        status = "SUSPICIOUS"
        severity = "HIGH"
        SUSPICIOUS_COUNT.inc()

    elif anomaly_score > 40:
        status = "SUSPICIOUS"
        severity = "MEDIUM"
        SUSPICIOUS_COUNT.inc()

    # ---------------- SAVE CSV ---------------- #

    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            house_id,
            usage,
            timestamp,
            status,
            baseline,
            anomaly_score,
            severity
        ])

    return jsonify({
        "message": "Data received",
        "status": status,
        "baseline": baseline,
        "anomaly_score": anomaly_score,
        "severity": severity
    })

@app.route("/alerts", methods=["GET"])
def alerts():

    alerts = []

    with open(CSV_FILE, "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row.get("status") == "SUSPICIOUS":
                alerts.append(row)

    return jsonify(alerts)

@app.route("/metrics")
def metrics():

    return Response(
        generate_latest(),
        mimetype="text/plain"
    )

# ---------------- MAIN ---------------- #

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

@app.route("/")
def home():
    return {
        "status": "running",
        "message": "Smart Electricity Theft Detection System is live"
    }