from typing import Dict, Any, List

ALLOPATHY_QUESTIONS = [
    {
        "id": "chief_complaint",
        "question_en": "What is the primary health problem that brought you to the hospital today?",
        "question_hi": "आज आप अस्पताल किस मुख्य तकलीफ के कारण आए हैं?",
        "options_en": ["Chest Pain", "Fever / Shivering", "Cough & Breathlessness", "Abdominal Pain", "Joint Pain", "Headache"],
        "options_hi": ["सीने में दर्द", "बुखार / कंपकंपी", "खांसी और सांस फूलना", "पेट में दर्द", "जोड़ों में दर्द", "सिरदर्द"]
    },
    {
        "id": "socrates_duration",
        "question_en": "How long have you had this problem?",
        "question_hi": "यह समस्या आपको कितने दिनों या महीनों से है?",
        "options_en": ["Less than 24 hours", "2 to 7 days", "1 to 4 weeks", "More than 1 month"],
        "options_hi": ["24 घंटे से कम", "2 से 7 दिन", "1 से 4 हफ्ते", "1 महीने से अधिक"]
    },
    {
        "id": "socrates_severity",
        "question_en": "How severe is your discomfort right now?",
        "question_hi": "आपकी तकलीफ अभी कितनी गंभीर है?",
        "options_en": ["Mild (Bearable)", "Moderate (Affects daily tasks)", "Severe (Unbearable)"],
        "options_hi": ["हल्की (सहनशील)", "मध्यम (कामकाज में परेशानी)", "गंभीर (असहनीय)"]
    },
    {
        "id": "past_history",
        "question_en": "Do you have any existing diagnosed medical conditions?",
        "question_hi": "क्या आपको पहले से कोई पुरानी बीमारी है?",
        "options_en": ["Diabetes Mellitus", "Hypertension (High BP)", "Thyroid Disorder", "Heart Disease", "None"],
        "options_hi": ["शुगर (डायबिटीज)", "हाई ब्लड प्रेशर (बीपी)", "थायराइड", "हृदय रोग", "कोई नहीं"]
    },
    {
        "id": "allergy_history",
        "question_en": "Are you allergic to any medicines (like Penicillin, Sulfa, Paracetamol)?",
        "question_hi": "क्या आपको किसी दवा (जैसे पेनिसिलिन, सल्फा) से कोई एलर्जी है?",
        "options_en": ["No Known Drug Allergies", "Penicillin / Antibiotic Allergy", "Painkiller / NSAID Allergy", "Skin Rash with Tablets"],
        "options_hi": ["कोई ज्ञात एलर्जी नहीं", "एंटीबायोटिक / पेनिसिलिन एलर्जी", "दर्द की दवा से एलर्जी", "दवा से त्वचा पर चकत्ते"]
    }
]

AYUSH_QUESTIONS = [
    {
        "id": "ayush_agni",
        "question_en": "How is your digestion and appetite (Agni Pariksha)?",
        "question_hi": "आपकी भूख और पाचन शक्ति कैसी है (अग्नि परीक्षा)?",
        "options_en": ["Sama Agni (Regular / Normal)", "Visham Agni (Irregular / Gas)", "Tikshna Agni (Intense / Acidic)", "Manda Agni (Sluggish / Heavy)"],
        "options_hi": ["सम अग्नि (सामान्य / संतुलित)", "विषम अग्नि (अनियमित / गैस)", "तीक्ष्ण अग्नि (तेज भूख / जलन)", "मंद अग्नि (धीमा पाचन / भारीपन)"]
    },
    {
        "id": "ayush_koshtha",
        "question_en": "How are your bowel movements (Koshtha Pariksha)?",
        "question_hi": "आपका पेट साफ होने की प्रकृति कैसी है (कोष्ठ परीक्षा)?",
        "options_en": ["Mrudu (Soft / Frequent)", "Madhyama (Regular / Normal)", "Krura (Hard / Constipated)"],
        "options_hi": ["मृदु (ढीला / बार-बार)", "मध्यम (नियमित / सामान्य)", "क्रूर (कब्ज / सख्त)"]
    },
    {
        "id": "ayush_prakriti",
        "question_en": "What is your physical tendency regarding climate and body build?",
        "question_hi": "मौसम और शारीरिक गठन के प्रति आपका स्वभाव क्या है (प्रकृति)?",
        "options_en": ["Vata (Dislikes Cold / Dry Skin)", "Pitta (Dislikes Heat / Easily Sweating)", "Kapha (Calm / Tolerates Weather Well)"],
        "options_hi": ["वात (ठंड नापसंद / रूखी त्वचा)", "पित्त (गर्मी नापसंद / पसीना अधिक)", "कफ (शांत स्वभाव / मजबूत शरीर)"]
    },
    {
        "id": "ayush_nidana",
        "question_en": "What best describes your regular diet and sleep habits (Ahara-Vihara)?",
        "question_hi": "आपका खान-पान और दिनचर्या कैसी है (आहार-विहार)?",
        "options_en": ["Timely meals, sound sleep", "Spicy / oily foods, late night sleep", "Skipping meals, stress / disturbed sleep"],
        "options_hi": ["समय पर भोजन, अच्छी नींद", "तीखा / तला-भुना, देर रात सोना", "अनियमित भोजन, तनाव / अधूरी नींद"]
    }
]

def get_next_question(department: str, answers: Dict[str, Any], lang: str = "en") -> Dict[str, Any]:
    question_pool = ALLOPATHY_QUESTIONS.copy()
    if department.upper() == "AYUSH":
        question_pool.extend(AYUSH_QUESTIONS)

    answered_ids = set(answers.keys())
    for q in question_pool:
        if q["id"] not in answered_ids:
            return {
                "question_id": q["id"],
                "question_text": q[f"question_{lang}"],
                "options": q[f"options_{lang}"],
                "is_complete": False
            }

    return {"question_id": "completed", "question_text": "Intake Complete", "options": [], "is_complete": True}

def generate_clinical_summary(session_data: Dict[str, Any]) -> Dict[str, Any]:
    answers = session_data.get("answers", {})
    docs = session_data.get("documents", [])
    dept = session_data.get("department", "General Medicine")

    all_labs = []
    all_meds = []
    all_diagnoses = []

    for d in docs:
        all_labs.extend(d.get("investigations", []))
        all_meds.extend(d.get("medications", []))
        all_diagnoses.extend(d.get("documented_diagnoses", []))

    abnormal_labs = [l for l in all_labs if l.get("is_abnormal")]

    summary_md = f"### CLINICAL INTAKE SUMMARY\n"
    summary_md += f"**Department:** {dept} | **Triage Status:** {session_data.get('triage_level', 'GREEN (Routine)')}\n\n"
    summary_md += f"**1. Chief Complaint & HPI:**\n"
    summary_md += f"- **Presenting Complaint:** {answers.get('chief_complaint', 'Not recorded')}\n"
    summary_md += f"- **Duration:** {answers.get('socrates_duration', 'Not recorded')}\n"
    summary_md += f"- **Severity:** {answers.get('socrates_severity', 'Not recorded')}\n\n"

    if dept.upper() == "AYUSH":
        summary_md += f"**2. Ayurvedic Pariksha (Dashavidha / Ahara-Vihara):**\n"
        summary_md += f"- **Agni:** {answers.get('ayush_agni', 'Not recorded')}\n"
        summary_md += f"- **Koshtha:** {answers.get('ayush_koshtha', 'Not recorded')}\n"
        summary_md += f"- **Constitutional Tendency (Prakriti):** {answers.get('ayush_prakriti', 'Not recorded')}\n"
        summary_md += f"- **Ahara-Vihara (Diet/Lifestyle Nidana):** {answers.get('ayush_nidana', 'Not recorded')}\n\n"

    summary_md += f"**3. Past Medical History & Comorbidities:**\n"
    past = answers.get('past_history', 'None')
    combined_history = list(set([past] + all_diagnoses))
    summary_md += f"- {', '.join([c for c in combined_history if c and c != 'None']) or 'No prior chronic conditions'}\n\n"

    summary_md += f"**4. Drug & Allergy Status:**\n"
    summary_md += f"- **Allergies:** {answers.get('allergy_history', 'No Known Drug Allergies')}\n"
    if all_meds:
        summary_md += f"- **Current/Prior Medications Extracted from Records:**\n"
        for m in all_meds[:5]:
            summary_md += f"  * {m.get('prescription_line')} ({m.get('frequency')})\n"
    else:
        summary_md += f"- **Prior Medications:** None documented in scanned records.\n"

    summary_md += f"\n**5. Prior Investigations & Flagged Lab Findings:**\n"
    if abnormal_labs:
        for l in abnormal_labs:
            summary_md += f"- ⚠️ **ABNORMAL:** {l['parameter']}: **{l['value']} {l['unit']}** (Ref: {l['reference_range']}) [{l['status']}]\n"
    else:
        summary_md += f"- No critical out-of-range lab values detected from uploaded records.\n"

    patient_audio_en = f"Intake complete. Your primary issue of {answers.get('chief_complaint', 'illness')} has been noted for the doctor."
    patient_audio_hi = f"आपकी प्रारंभिक जानकारी दर्ज कर ली गई है। मुख्य शिकायत {answers.get('chief_complaint', 'तकलीफ')} डॉक्टर के स्क्रीन पर भेज दी गई है।"

    return {
        "physician_summary_markdown": summary_md,
        "patient_audio_confirmation": {
            "en": patient_audio_en,
            "hi": patient_audio_hi
        },
        "abnormal_labs": abnormal_labs,
        "red_flag_alert": session_data.get("is_emergency", False)
    }
