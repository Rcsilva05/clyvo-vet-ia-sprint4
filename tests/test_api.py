from app import app


def test_health_and_pets_endpoints():
    client = app.test_client()

    health = client.get("/health")
    pets = client.get("/api/pets")

    assert health.status_code == 200
    assert health.get_json()["status"] == "ok"
    assert pets.status_code == 200
    assert len(pets.get_json()) == 3


def test_recommendation_api_validates_pet_id_and_discloses_simulated_data(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    client = app.test_client()

    missing_id = client.post("/api/recommendation", json={})
    invalid_body = client.post("/api/recommendation", json=["pet-003"])
    unknown_pet = client.post("/api/recommendation", json={"petId": "unknown"})
    valid = client.post("/api/recommendation", json={"petId": "pet-003"})

    assert missing_id.status_code == 400
    assert invalid_body.status_code == 400
    assert unknown_pet.status_code == 404
    assert valid.status_code == 200
    result = valid.get_json()
    assert result["pet"]["name"] == "Mimi"
    assert result["data_source"] == "simulated"
    assert result["llm_mode"] == "rules_only"
    assert "não é diagnóstico" in result["disclaimer"]
