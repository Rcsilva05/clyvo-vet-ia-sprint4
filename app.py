import os
from flask import Flask, jsonify, render_template, request

from src.ia_engine import build_api_response, list_pets

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html", pets=list_pets())


@app.get("/api/pets")
def api_pets():
    return jsonify(list_pets())


@app.post("/api/recommendation")
def api_recommendation():
    payload = request.get_json(silent=True) or {}
    if not isinstance(payload, dict):
        return jsonify({"error": "request body must be a JSON object"}), 400
    pet_id = payload.get("petId")
    if not pet_id:
        return jsonify({"error": "petId is required"}), 400

    try:
        return jsonify(build_api_response(pet_id))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "clyvo-vet-ia"})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
