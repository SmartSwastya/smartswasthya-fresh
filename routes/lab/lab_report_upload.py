# route/lab/lab_report_upload.py

# ╔════════════════════════════════════════════════╗
# ║ SECTION: Imports                               ║
# ╚════════════════════════════════════════════════╝
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/lab/report/upload")
def upload_lab_report(patient_id: int, file: UploadFile = File(...)):
    return JSONResponse(content={"status": "uploaded", "filename": file.filename, "patient_id": patient_id})
