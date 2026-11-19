from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="MediKiosk Clinical History & ABDM API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AyushPariksha(BaseModel):
    prakriti: str
    agni: str
    koshtha: str
    nidana: Optional[str] = ""


class PatientCase(BaseModel):
    patient_name: str
    age: int
    gender: str
    abha_id: Optional[str] = "Unlinked"
    department: Optional[str] = "General Medicine"
    complaint: str
    duration: str
    hpi_onset: Optional[str] = "Gradual over days"
    hpi_character: Optional[str] = "Not specified"
    hpi_severity: int = 5
    assoc_symptoms: List[str] = []
    comorbidities: List[str] = []
    past_history: Optional[str] = "None"
    current_meds: Optional[str] = "None"
    allergies: Optional[str] = "NKDA"
    opd_mode: str = "allopathic"
    priority: bool = False
    ayush: Optional[AyushPariksha] = None
    docs: List[Dict[str, Any]] = []


class DoctorVerification(BaseModel):
    doctor_notes: str


cases_db: List[Dict[str, Any]] = []


@app.get("/")
def read_root():
    return {"status": "MediKiosk OPD Backend is running successfully!"}


@app.get("/api/cases")
def list_cases():
    sorted_cases = sorted(cases_db, key=lambda c: c["priority"], reverse=True)
    return {"count": len(sorted_cases), "cases": sorted_cases}


@app.post("/api/patient/intake")
def receive_patient_case(data: PatientCase):
    case_id = f"OPD-{101 + len(cases_db)}"
    priority_count = sum(1 for c in cases_db if c["priority"])
    token = (
        f"P-{priority_count + 1:02d} (PRIORITY)"
        if data.priority
        else f"R-{14 + len(cases_db)}"
    )

    record = {
        "id": case_id,
        "token": token,
        "verified": False,
        "doctor_notes": "",
        **data.model_dump(),
    }
    cases_db.insert(0, record)

    return {
        "status": "Success",
        "message": f"Case recorded for {data.patient_name} — Token {token}",
        "case": record,
    }


@app.patch("/api/cases/{case_id}/verify")
def verify_case(case_id: str, payload: DoctorVerification):
    for case in cases_db:
        if case["id"] == case_id:
            case["doctor_notes"] = payload.doctor_notes
            case["verified"] = True
            return {"status": "Verified", "case": case}
    raise HTTPException(status_code=404, detail="Case not found")