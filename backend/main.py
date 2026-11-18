from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Patient Case Taking API", version="1.0")

# Enable CORS so your frontend can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local testing
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],  # Allows all headers
)

class PatientCase(BaseModel):
    patient_name: str
    age: int
    gender: str
    complaint: str
    duration: str

@app.get("/")
def read_root():
    return {"status": "OPD Backend is running successfully!"}

@app.post("/api/patient/intake")
def receive_patient_case(data: PatientCase):
    structured_summary = {
        "status": "Success",
        "message": f"Case successfully recorded and structured for {data.patient_name}",
        "data": data.dict()
    }
    return structured_summary