import re
from typing import Dict, List

RED_FLAG_RULES = [
    {
        "category": "Cardiovascular / Acute Coronary Syndrome",
        "keywords": [
            "chest pain", "chest tightness", "chest pressure", "pain radiating to left arm",
            "chhati me dard", "chhati me dabav", "heart attack", "sweating with chest pain"
        ],
        "required_combinations": [
            ["chest pain", "sweat"],
            ["chest pain", "breathless"],
            ["chest pain", "arm"],
            ["chhati me dard", "paseena"],
            ["chhati me dard", "saas"]
        ],
        "action": "IMMEDIATE CODE RED: Direct patient to Casualty / Emergency Room. ECG within 10 minutes."
    },
    {
        "category": "Neurological / Acute Stroke (FAST)",
        "keywords": [
            "facial drooping", "face deviation", "arm weakness", "sudden numbness",
            "slurred speech", "unable to speak", "muh tedha", "bol nahi pa rahe", "haath sunn"
        ],
        "required_combinations": [
            ["weakness", "speech"],
            ["face", "speech"],
            ["slurred", "arm"],
            ["bol", "kamzori"]
        ],
        "action": "IMMEDIATE STROKE ALERT: Priority triage for non-contrast CT Brain & thrombolysis assessment."
    },
    {
        "category": "Severe Respiratory Distress",
        "keywords": [
            "severe breathlessness", "gasping for air", "blue lips", "unable to speak full sentences",
            "saas phoolna", "dam ghutna", "neela padna"
        ],
        "required_combinations": [
            ["saas", "bahut"],
            ["breathless", "severe"],
            ["lips", "blue"]
        ],
        "action": "IMMEDIATE OXYGEN SUPPORT: SpO2 evaluation, high-flow O2, emergency physician review."
    },
    {
        "category": "Severe Sepsis / Altered Mental Status",
        "keywords": [
            "unconscious", "altered sensorium", "confusion with fever", "lethargic",
            "behosh", "hosh kho dena", "bhatakna"
        ],
        "required_combinations": [
            ["fever", "confusion"],
            ["bukhar", "behosh"],
            ["fever", "unconscious"]
        ],
        "action": "PRIORITY RESUSCITATION: IV access, blood cultures, urgent physician bedside evaluation."
    },
    {
        "category": "Acute Abdomen / Severe Hemorrhage",
        "keywords": [
            "vomiting blood", "blood in stool", "rigid abdomen", "extreme sudden stomach pain",
            "khoon ki ulti", "khoon aana", "pet me bhayanak dard"
        ],
        "required_combinations": [
            ["vomit", "blood"],
            ["ulti", "khoon"],
            ["stool", "blood"]
        ],
        "action": "EMERGENCY SURGICAL / GI CONSULT: Resuscitation, urgent ultrasound / surgical evaluation."
    }
]

def evaluate_red_flags(text: str) -> Dict:
    clean_text = text.lower().strip()
    matched_flags = []
    actions = []

    for rule in RED_FLAG_RULES:
        is_matched = any(kw in clean_text for kw in rule["keywords"])
        if not is_matched and "required_combinations" in rule:
            for combo in rule["required_combinations"]:
                if all(term in clean_text for term in combo):
                    is_matched = True
                    break

        if is_matched:
            matched_flags.append(rule["category"])
            actions.append(rule["action"])

    return {
        "is_emergency": len(matched_flags) > 0,
        "matched_categories": matched_flags,
        "recommended_actions": actions,
        "triage_level": "RED (Emergency)" if len(matched_flags) > 0 else "GREEN (Routine Intake)"
    }
