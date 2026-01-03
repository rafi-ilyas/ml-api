from flask import Flask, request, jsonify
import joblib, time, numpy as np

app = Flask(__name__)
model = joblib.load("model.pkl")

devices = {}
manual_control = {}

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    device = data["device_id"]

    X = np.array([[data["suhu"], data["kelembapan"], data["cahaya"], data["udara"], data["kebisingan"]]])
    pred = model.predict(X)[0]

    kenyamanan = "nyaman" if pred == 1 else "tidak_nyaman"

    action = {
        "lampu": "on" if data["cahaya"] < 2000 else "off",
        "ac": "off" if data["suhu"] > 30 else "on",
        "peringatan": "gas_bocor" if data["udara"] > 2500 else "aman"
    }

    devices[device] = {
        "kenyamanan": kenyamanan,
        "action": action,
        "last_update": time.strftime("%H:%M:%S")
    }

    return jsonify(devices[device])

@app.route("/status", methods=["GET"])
def status():
    return jsonify(devices)

@app.route("/control/<device>", methods=["POST"])
def control(device):
    manual_control[device] = request.json
    return {"status":"ok"}

@app.route("/control/<device>", methods=["GET"])
def get_control(device):
    return jsonify(manual_control.get(device, {}))

if __name__ == "__main__":
    app.run()