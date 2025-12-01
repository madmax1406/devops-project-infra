from flask import Flask, request, jsonify, render_template
from prometheus_client import generate_latest, Gauge, Counter
import time

app = Flask(__name__)

# --- Prometheus Metrics ---
REQUEST_COUNT = Counter("pacer_requests_total", "Total API requests")
LAST_REQUEST_TIME = Gauge("pacer_last_request_timestamp", "Last request timestamp")

# --- Home Page ---
@app.route("/")
def home():
    return render_template("index.html")

# --- Health & Liveness ---
@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/readiness")
def readiness():
    return jsonify({"ready": True}), 200

# --- Metrics ---
@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": "text/plain"}

# --- Pace Calculation ---
@app.route("/pace", methods=["POST"])
def pace():
    REQUEST_COUNT.inc()
    LAST_REQUEST_TIME.set(time.time())

    race = request.form.get("race")
    hours = int(request.form.get("hours", 0))
    minutes = int(request.form.get("minutes", 0))
    seconds = int(request.form.get("seconds", 0))

    total_seconds = hours * 3600 + minutes * 60 + seconds

    race_distances = {
        "Marathon": 42.195,
        "Half Marathon": 21.097,
        "10K": 10,
        "5K": 5
    }

    distance = race_distances.get(race)

    pace_per_km = total_seconds / distance
    pace_min = int(pace_per_km // 60)
    pace_sec = int(pace_per_km % 60)

    splits = []
    cumulative = 0
    for km in range(1, int(distance) + 1):
        cumulative += pace_per_km
        splits.append({
            "km": km,
            "split": f"{pace_min}:{pace_sec:02d}",
            "cumulative": f"{int(cumulative//60)}:{int(cumulative%60):02d}",
        })

    return render_template("result.html",
                           race=race,
                           total_time=f"{hours}h {minutes}m {seconds}s",
                           pace=f"{pace_min}:{pace_sec:02d}",
                           splits=splits)

# -------------------------
# Flask Entrypoint
# -------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
