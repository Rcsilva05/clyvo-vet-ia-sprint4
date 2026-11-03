PETS = [
    {
        "id": "pet-001",
        "name": "Luna",
        "species": "Cachorro",
        "breed": "Shih Tzu",
        "age_months": 72,
        "weight_kg": 7.2,
        "conditions": ["incontinência leve", "sensibilidade urinária"],
        "medications": ["suplemento de água"],
        "urine_pattern": "frequente",
    },
    {
        "id": "pet-002",
        "name": "Thor",
        "species": "Cachorro",
        "breed": "Pastor Alemão",
        "age_months": 48,
        "weight_kg": 28.5,
        "conditions": ["disúria recorrente"],
        "medications": ["antibiótico profilático"],
        "urine_pattern": "normal",
    },
    {
        "id": "pet-003",
        "name": "Mimi",
        "species": "Gato",
        "breed": "Siames",
        "age_months": 120,
        "weight_kg": 4.4,
        "conditions": ["hipertensão", "obesidade leve"],
        "medications": ["medicação para pressão"],
        "urine_pattern": "ausente",
    },
]

EVENTS = {
    "pet-001": [
        {"type": "uria_frequente", "timestamp": "2026-10-30T08:00:00", "intensity": 7},
        {"type": "uria_frequente", "timestamp": "2026-10-30T18:30:00", "intensity": 8},
        {"type": "uria_frequente", "timestamp": "2026-11-02T08:15:00", "intensity": 7},
        {"type": "beber_muita_agua", "timestamp": "2026-11-02T09:00:00", "intensity": 6},
    ],
    "pet-002": [
        {"type": "urinou_norma", "timestamp": "2026-11-02T07:00:00", "intensity": 2},
        {"type": "urinou_norma", "timestamp": "2026-11-02T18:00:00", "intensity": 2},
    ],
    "pet-003": [
        {"type": "sem_urina", "timestamp": "2026-11-02T12:00:00", "intensity": 9},
        {"type": "sem_urina", "timestamp": "2026-11-02T18:00:00", "intensity": 9},
        {"type": "beber_muita_agua", "timestamp": "2026-11-02T17:00:00", "intensity": 7},
    ],
}
