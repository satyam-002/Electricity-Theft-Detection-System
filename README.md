# ⚡ Smart Electricity Theft Detection System

A real-time electricity monitoring and anomaly detection system built using Flask, Prometheus, Grafana, and Docker.

This project simulates smart meter telemetry data, processes electricity consumption patterns, detects suspicious usage anomalies, and visualizes live analytics through a monitoring dashboard.

---

# 🚀 Features

- Real-time electricity telemetry simulation
- REST API ingestion layer using Flask
- Rule-based anomaly detection engine
- Behavioral baseline comparison
- Suspicious event classification
- Prometheus metrics integration
- Grafana live monitoring dashboard
- Dockerized monitoring stack

---

# 🧠 Detection Logic

The system compares incoming electricity usage with predefined historical baselines for each house.

If the deviation exceeds threshold levels:
- MEDIUM severity anomaly detected
- HIGH severity anomaly detected

This simulates electricity theft or abnormal consumption behavior.

---

# 🏗️ System Architecture

```text
Telemetry Simulator
        ↓
Flask Ingestion API
        ↓
Behavioral Analysis Engine
        ↓
Prometheus Metrics
        ↓
Grafana Dashboard
