import os
import uuid
import shutil
from typing import Dict, Any, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.triage_engine import evaluate_red_flags
from backend.ocr_engine import process_medical_document, parse_clinical_entities
from backend.clinical_engine import get_next_question, generate_clinical_summary
from backend.fhir_exporter import create_abdm_fhir_bundle
from backend.config import settings

app = FastAPI(title="MediKiosk Clinical Intake System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ACTIVE_SESSIONS: Dict[str, Dict[str, Any]] = {}

class SessionStartRequest(BaseModel):
    patient_name: str
    abha_id: Optional[str] = "ABHA-91-XXXX-XXXX-XXXX"
    language: str = "en"
    department: str = "General Medicine"
    consent_granted: bool = True

class AnswerRequest(BaseModel):
    session_id: str
    question_id: str
    answer_text: str

@app.get("/health")
def health():
    return {"status": "ok", "provider": settings.LLM_PROVIDER, "version": "1.0.0"}

@app.post("/api/session/start")
def start_session(req: SessionStartRequest):
    session_id = str(uuid.uuid4())
    ACTIVE_SESSIONS[session_id] = {
        "session_id": session_id,
        "patient_name": req.patient_name,
        "abha_id": req.abha_id,
        "language": req.language,
        "department": req.department,
        "consent": req.consent_granted,
        "answers": {},
        "documents": [],
        "is_emergency": False,
        "triage_level": "GREEN (Routine)"
    }
    next_q = get_next_question(req.department, {}, req.language)
    return {"session_id": session_id, "first_question": next_q}

@app.post("/api/chat/submit-answer")
def submit_answer(req: AnswerRequest):
    session = ACTIVE_SESSIONS.get(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or expired")

    session["answers"][req.question_id] = req.answer_text

    triage = evaluate_red_flags(req.answer_text)
    if triage["is_emergency"]:
        session["is_emergency"] = True
        session["triage_level"] = triage["triage_level"]
        return {
            "emergency_alert": True,
            "triage": triage,
            "message": "EMERGENCY SYMPTOM DETECTED: Proceed immediately to the Casualty Desk."
        }

    next_q = get_next_question(session["department"], session["answers"], session["language"])
    return {
        "emergency_alert": False,
        "next_question": next_q
    }

@app.post("/api/documents/upload")
async def upload_document(
    session_id: str = Form(...),
    file: Optional[UploadFile] = File(None),
    raw_text: Optional[str] = Form(None)
):
    session = ACTIVE_SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if file:
        temp_path = f"/tmp/{uuid.uuid4()}_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        doc_result = process_medical_document(image_path=temp_path, doc_name=file.filename)
        try:
            os.remove(temp_path)
        except Exception:
            pass
    elif raw_text:
        doc_result = parse_clinical_entities(raw_text, doc_name="Prescription / Report Note")
    else:
        raise HTTPException(status_code=400, detail="Provide an image file or text")

    session["documents"].append(doc_result)
    return {
        "status": "Document ingested",
        "extracted_data": doc_result
    }

@app.post("/api/summary/finalize")
def finalize_summary(session_id: str):
    session = ACTIVE_SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    summary_bundle = generate_clinical_summary(session)
    session["summary"] = summary_bundle
    return summary_bundle

@app.get("/api/physician/summary/{session_id}")
def get_physician_view(session_id: str):
    session = ACTIVE_SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        "session": session,
        "summary": session.get("summary") or generate_clinical_summary(session)
    }

@app.get("/api/fhir/export/{session_id}")
def export_fhir(session_id: str):
    session = ACTIVE_SESSIONS.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return create_abdm_fhir_bundle(session)

@app.delete("/api/session/purge/{session_id}")
def purge_session(session_id: str):
    if session_id in ACTIVE_SESSIONS:
        del ACTIVE_SESSIONS[session_id]
    return {"status": "Session data scrubbed from memory"}

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_path = os.path.join(base_dir, "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
