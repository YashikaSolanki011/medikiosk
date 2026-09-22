import uuid
from datetime import datetime
from typing import Dict, Any

def create_abdm_fhir_bundle(session_data: Dict[str, Any]) -> Dict[str, Any]:
    bundle_id = str(uuid.uuid4())
    patient_id = str(uuid.uuid4())
    composition_id = str(uuid.uuid4())
    now_iso = datetime.utcnow().isoformat() + "Z"

    masked_abha = session_data.get("abha_id", "ABHA-91-XXXX-XXXX-XXXX")

    bundle = {
        "resourceType": "Bundle",
        "id": bundle_id,
        "meta": {
            "versionId": "1",
            "lastUpdated": now_iso,
            "profile": ["https://nrces.in/ndhm/fhir/r4/StructureDefinition/DocumentBundle"]
        },
        "identifier": {
            "system": "https://healthid.ndhm.gov.in",
            "value": bundle_id
        },
        "type": "document",
        "timestamp": now_iso,
        "entry": [
            {
                "fullUrl": f"urn:uuid:{composition_id}",
                "resource": {
                    "resourceType": "Composition",
                    "id": composition_id,
                    "status": "final",
                    "type": {
                        "coding": [{
                            "system": "http://snomed.info/sct",
                            "code": "371530004",
                            "display": "Clinical consultation report"
                        }],
                        "text": "Clinical Intake OPD Summary"
                    },
                    "subject": {"reference": f"urn:uuid:{patient_id}"},
                    "date": now_iso,
                    "title": "MediKiosk OPD Clinical Intake Record",
                    "section": [
                        {
                            "title": "Chief Complaints",
                            "text": {
                                "status": "generated",
                                "div": f"<div>{session_data.get('answers', {}).get('chief_complaint', 'Unspecified')}</div>"
                            }
                        }
                    ]
                }
            },
            {
                "fullUrl": f"urn:uuid:{patient_id}",
                "resource": {
                    "resourceType": "Patient",
                    "id": patient_id,
                    "identifier": [{
                        "type": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/v2-0203", "code": "MR"}]},
                        "system": "https://healthid.ndhm.gov.in",
                        "value": masked_abha
                    }],
                    "name": [{"text": session_data.get("patient_name", "Patient")}],
                    "gender": session_data.get("gender", "unknown")
                }
            }
        ]
    }
    return bundle
