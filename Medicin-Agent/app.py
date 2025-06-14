from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import List, Optional
import requests
import json
import aiofiles
import os
from pydantic import BaseModel
from agent.agent import diagnosis_chain
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = FastAPI()

# Configuration
TEMP_STORAGE = "temp_uploads"
os.makedirs(TEMP_STORAGE, exist_ok=True)


# First API: Diagnosis Endpoint ========================================
class DiagnosisRequest(BaseModel):
    symptoms: str
    medical_history: Optional[str] = None
    lab_reports_text: Optional[str] = None


async def process_report_file(file: UploadFile) -> str:
    """Send a single report file to the medical report API and return stringified JSON."""
    try:
        temp_path = os.path.join(TEMP_STORAGE, file.filename)

        # Save the file temporarily
        async with aiofiles.open(temp_path, "wb") as out_file:
            await out_file.write(await file.read())

        # Call the Medical Report API
        with open(temp_path, "rb") as f:
            response = requests.post(
                "http://0.0.0.0:8000/get-medical-report-info/",
                files={"files": (file.filename, f, file.content_type)},  # Corrected key
            )

        # Clean up temporary file
        os.remove(temp_path)

        # Handle response
        if response.status_code != 200:
            raise HTTPException(
                status_code=400, detail=f"Medical API error: {response.text}"
            )

        return json.dumps(response.json())  # Convert JSON to string

    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(
            status_code=500, detail=f"Report processing error: {str(e)}"
        )


@app.post("/diagnose/")
async def diagnose(
    patient_info: str = Form(default=""),
    symptoms: str = Form(default=""),
    medical_history: str = Form(None),
    allergies: str = Form(None),
    current_medications: str = Form(None),
    diagnosis: str = Form(None),
    additional_context: str = Form(None)
):
    try:
        response =  diagnosis_chain.invoke(
            {
                "patient_info": patient_info,
                "symptoms": symptoms,
                "additional_context": additional_context,
                "history": medical_history,
                "diagnosis": diagnosis,
                "current_medications": current_medications,
                "allergies": allergies,
            }
        )

        # If it's an object with .content attribute
        return  response.content

    except Exception as e:
        logger.exception("Error during diagnosis_chain.ainvoke")
        raise HTTPException(status_code=500, detail="Internal diagnosis engine error")
