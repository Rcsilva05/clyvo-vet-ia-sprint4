from __future__ import annotations

import os
from typing import Any, Dict, List

import requests

from src.sample_data import EVENTS, PETS


EVENT_WEIGHTS = {
    "uria_frequente": 18,
    "beber_muita_agua": 12,
    "sem_urina": 22,
    "urinou_norma": -10,
}

CONDITION_WEIGHTS = {
    "incontinência leve": 10,
    "sensibilidade urinária": 12,
    "disúria recorrente": 16,
    "hipertensão": 10,
    "obesidade leve": 6,
}


def _risk_profile(score: int) -> str:
    if score >= 75:
        return "Crítica"
    if score >= 50:
        return "Alta"
    if score >= 25:
        return "Média"
    return "Baixa"


def _normalize_pet(pet: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": pet.get("id", "unknown"),
        "name": pet.get("name", "Pet"),
        "species": pet.get("species", "Pet"),
        "breed": pet.get("breed", "Sem raça informada"),
        "age_months": int(pet.get("age_months", 0)),
        "weight_kg": float(pet.get("weight_kg", 0.0)),
        "conditions": pet.get("conditions", []),
        "medications": pet.get("medications", []),
        "urine_pattern": pet.get("urine_pattern", "normal"),
    }


def calculate_risk_score(pet: Dict[str, Any], events: List[Dict[str, Any]]) -> int:
    pet = _normalize_pet(pet)
    score = 0

    if pet["age_months"] >= 96:
        score += 10
    if pet["weight_kg"] >= 25:
        score += 8
    if pet["urine_pattern"] == "ausente":
        score += 14
    if pet["urine_pattern"] == "frequente":
        score += 12

    for condition in pet["conditions"]:
        score += CONDITION_WEIGHTS.get(condition, 4)

    if pet["medications"]:
        score += max(4, len(pet["medications"]) * 3)

    for event in events:
        event_type = event.get("type", "")
        intensity = int(event.get("intensity", 0))
        score += EVENT_WEIGHTS.get(event_type, 0) + intensity

    if len(events) >= 3:
        score += 10

    return max(0, min(100, score))


def build_recommendation(pet: Dict[str, Any], events: List[Dict[str, Any]]) -> Dict[str, Any]:
    pet = _normalize_pet(pet)
    score = calculate_risk_score(pet, events)
    level = _risk_profile(score)

    if level == "Crítica":
        tutor_message = (
            f"{pet['name']} está com risco {level.lower()} de problemas urinários. "
            "Procure um veterinário com urgência e observe se há dor ou sinais de desidratação."
        )
        clinic_message = (
            "Risco crítico por padrão de micção anormal, possível urgência clínica. "
            "Recomendar avaliação imediata e monitoramento laboratorial se houver dor ou febre."
        )
        action = "Avaliação imediata com atendimento veterinário"
    elif level == "Alta":
        tutor_message = (
            f"{pet['name']} está com risco {level.lower()} e merece atenção nas próximas 24h. "
            "Reduza o acesso a água em excesso e registe as próximas micções."
        )
        clinic_message = (
            "Risco elevado por frequência anormal de micção e histórico relevante. "
            "Recomendar revisão do histórico clínico e avaliação de rotina."
        )
        action = "Reavaliação em até 24 horas"
    elif level == "Média":
        tutor_message = (
            f"{pet['name']} pode ter uma variação de rotina urinária. "
            "Continue monitorando a frequência e observe qualquer dor ou alteração no comportamento."
        )
        clinic_message = (
            "Risco moderado: padrão de micção alterado, mas sem urgência emergencial. "
            "Seguir monitoramento e considerar ajuste de protocolo de acompanhamento."
        )
        action = "Acompanhamento de rotina"
    else:
        tutor_message = (
            f"{pet['name']} está com padrão urinário dentro do esperado, mas é importante manter o acompanhamento."
        )
        clinic_message = (
            "Padrão estável, sem sinais de urgência. Continuar acompanhamento preventivo."
        )
        action = "Manter monitoramento e rotina do tutor"

    return {
        "pet": pet,
        "risk_score": score,
        "priority": level,
        "recommendation": action,
        "tutor_summary": tutor_message,
        "clinical_summary": clinic_message,
    }


def get_pet_by_id(pet_id: str) -> Dict[str, Any]:
    for pet in PETS:
        if pet["id"] == pet_id:
            return pet
    raise ValueError(f"Pet {pet_id} not found")


def get_recommendation_for_pet(pet_id: str) -> Dict[str, Any]:
    pet = get_pet_by_id(pet_id)
    events = EVENTS.get(pet_id, [])
    return build_recommendation(pet, events)


def _build_llm_prompt(pet: Dict[str, Any], recommendation: Dict[str, Any]) -> str:
    return (
        "Você é um assistente veterinário que traduz recomendações de saúde para tutor e clínica.\n"
        f"Pet: {pet['name']} ({pet['species']} {pet['breed']})\n"
        f"Idade: {pet['age_months']} meses\n"
        f"Condições: {', '.join(pet['conditions']) or 'nenhuma'}\n"
        f"Risco: {recommendation['risk_score']} / 100\n"
        f"Prioridade: {recommendation['priority']}\n"
        "Escreva um resumo claro, empático e profissional para o tutor e outro para a clínica."
    )


def generate_llm_summary(pet: Dict[str, Any], recommendation: Dict[str, Any]) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return recommendation

    payload = {
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "messages": [
            {"role": "system", "content": "Você é um assistente veterinário especialista em IA para saúde animal."},
            {"role": "user", "content": _build_llm_prompt(pet, recommendation)},
        ],
        "temperature": 0.4,
    }

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=20,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        recommendation["llm_summary"] = content.strip()
        recommendation["llm_mode"] = "openai"
        return recommendation
    except Exception:
        recommendation["llm_mode"] = "offline_fallback"
        recommendation["llm_summary"] = "Resumo offline: IA local ativada; integração externa não configurada."
        return recommendation


def build_api_response(pet_id: str) -> Dict[str, Any]:
    pet = get_pet_by_id(pet_id)
    events = EVENTS.get(pet_id, [])
    recommendation = build_recommendation(pet, events)
    return generate_llm_summary(pet, recommendation)


def list_pets() -> List[Dict[str, Any]]:
    return PETS
