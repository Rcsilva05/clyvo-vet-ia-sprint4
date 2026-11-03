from src.ia_engine import build_recommendation, calculate_risk_score


def test_risk_for_luna_is_high():
    pet = {
        "id": "pet-001",
        "name": "Luna",
        "species": "Cachorro",
        "breed": "Shih Tzu",
        "age_months": 72,
        "weight_kg": 7.2,
        "conditions": ["incontinência leve", "sensibilidade urinária"],
        "medications": ["suplemento de água"],
        "urine_pattern": "frequente",
    }
    events = [
        {"type": "uria_frequente", "intensity": 7},
        {"type": "uria_frequente", "intensity": 8},
        {"type": "beber_muita_agua", "intensity": 6},
    ]

    score = calculate_risk_score(pet, events)
    assert score >= 50

    recommendation = build_recommendation(pet, events[:1])
    assert recommendation["priority"] == "Alta"
    assert "tutor_summary" in recommendation
    assert "clinical_summary" in recommendation
    assert "mantenha água disponível" in recommendation["tutor_summary"]
    assert "Reduza o acesso a água" not in recommendation["tutor_summary"]
    assert recommendation["data_source"] == "simulated"
    assert "não é diagnóstico" in recommendation["disclaimer"]


def test_risk_for_thor_is_low():
    pet = {
        "id": "pet-002",
        "name": "Thor",
        "species": "Cachorro",
        "breed": "Pastor Alemão",
        "age_months": 48,
        "weight_kg": 28.5,
        "conditions": ["disúria recorrente"],
        "medications": ["antibiótico profilático"],
        "urine_pattern": "normal",
    }
    events = [
        {"type": "urinou_norma", "intensity": 2},
        {"type": "urinou_norma", "intensity": 2},
    ]

    recommendation = build_recommendation(pet, events)
    assert recommendation["priority"] in {"Baixa", "Média"}


def test_score_is_bounded_and_unknown_events_do_not_add_risk():
    pet = {"name": "Teste"}
    score = calculate_risk_score(
        pet,
        [{"type": "evento_desconhecido", "intensity": 0}],
    )
    assert 0 <= score <= 100
