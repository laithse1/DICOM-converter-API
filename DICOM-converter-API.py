from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Dict
import os
import shutil
import tempfile
import pydicom
from PIL import Image
from pydicom.pixel_data_handlers.util import apply_voi_lut
import logging
import cv2
from reportlab.pdfgen import canvas
from tifffile import imwrite

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize FastAPI app
app = FastAPI(title="Enhanced DICOM Converter API", description="API to convert DICOM files to various formats and extract metadata.")

# Temporary directory for file processing
temp_dir = tempfile.mkdtemp()

def decode_pixel_data(dicom):
    """Decode pixel data, handling compressed formats correctly."""
    dicom.decode()  # Ensure compressed data is decoded
    image_data = apply_voi_lut(dicom.pixel_array, dicom)

    if dicom.PhotometricInterpretation == 'YBR_FULL_422':
        return Image.fromarray(image_data, mode='YCbCr').convert('RGB')
    else:
        return Image.fromarray(image_data)

def dicom_to_format(dicom_file: UploadFile, output_folder: str, format: str, quality: int = 95) -> str:
    """Convert DICOM to the specified format."""
    try:
        input_path = os.path.join(output_folder, dicom_file.filename)
        with open(input_path, "wb") as f:
            shutil.copyfileobj(dicom_file.file, f)

        dicom = pydicom.dcmread(input_path, force=True)

        if format in ["jpeg", "png", "gif"]:
            image = decode_pixel_data(dicom)
            output_path = os.path.join(output_folder, dicom_file.filename.replace(".dcm", f".{format}"))
            image.save(output_path, format.upper(), quality=quality)
        elif format == "mp4":
            frames = dicom.pixel_array
            height, width = frames[0].shape
            output_path = os.path.join(output_folder, dicom_file.filename.replace(".dcm", ".mp4"))
            video_writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), 10, (width, height))
            for frame in frames:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
                video_writer.write(rgb_frame)
            video_writer.release()
        elif format == "pdf":
            image = decode_pixel_data(dicom)
            output_path = os.path.join(output_folder, dicom_file.filename.replace(".dcm", ".pdf"))
            pdf = canvas.Canvas(output_path)
            metadata = f"Patient Name: {dicom.PatientName}\nStudy Date: {dicom.StudyDate}\n"
            pdf.drawString(50, 800, metadata)
            temp_image_path = os.path.join(output_folder, "temp_image.jpg")
            image.save(temp_image_path, "JPEG")
            pdf.drawImage(temp_image_path, 50, 600, width=500, height=500)
            pdf.save()
            os.remove(temp_image_path)
        elif format == "tiff":
            frames = dicom.pixel_array
            output_path = os.path.join(output_folder, dicom_file.filename.replace(".dcm", ".tiff"))
            imwrite(output_path, frames)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported format: {format}")

        logging.info(f"Converted {dicom_file.filename} to {format.upper()}.")
        return output_path
    except Exception as e:
        logging.error(f"Error converting {dicom_file.filename} to {format.upper()}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to convert {dicom_file.filename} to {format.upper()}: {str(e)}")

def extract_metadata(dicom_file: UploadFile) -> Dict:
    """Extract metadata from a DICOM file."""
    try:
        dicom = pydicom.dcmread(dicom_file.file, force=True)
        metadata = {
            "PatientName": str(dicom.get("PatientName", "Unknown")),
            "PatientID": str(dicom.get("PatientID", "Unknown")),
            "StudyDate": str(dicom.get("StudyDate", "Unknown")),
            "Modality": str(dicom.get("Modality", "Unknown")),
            "StudyDescription": str(dicom.get("StudyDescription", "Unknown")),
            "Manufacturer": str(dicom.get("Manufacturer", "Unknown")),
        }
        logging.info(f"Extracted metadata from {dicom_file.filename}.")
        return metadata
    except Exception as e:
        logging.error(f"Error extracting metadata from {dicom_file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to extract metadata: {str(e)}")

@app.post("/convert", response_class=JSONResponse)
async def convert_dicom(file: UploadFile = File(...), format: str = "jpeg", quality: int = 95):
    """Convert a single DICOM file to the specified format."""
    output_path = dicom_to_format(file, temp_dir, format, quality)
    return {"file_path": output_path}

@app.post("/convert-batch", response_model=List[dict])
async def batch_convert_dicom(files: List[UploadFile] = File(...), formats: List[str] = ["jpeg"], quality: int = 95):
    """Batch convert multiple DICOM files to multiple formats."""
    results = []
    for file in files:
        file_results = {"input_file": file.filename, "outputs": []}
        for format in formats:
            try:
                output_path = dicom_to_format(file, temp_dir, format, quality)
                file_results["outputs"].append({"format": format, "file_path": output_path})
            except HTTPException as e:
                file_results["outputs"].append({"format": format, "error": str(e.detail)})
        results.append(file_results)
    return results

@app.post("/metadata", response_model=Dict)
async def get_metadata(file: UploadFile = File(...)):
    """Extract metadata from a single DICOM file."""
    metadata = extract_metadata(file)
    return metadata

@app.post("/metadata-batch", response_model=List[Dict])
async def get_metadata_batch(files: List[UploadFile] = File(...)):
    """Extract metadata from multiple DICOM files."""
    results = []
    for file in files:
        try:
            metadata = extract_metadata(file)
            results.append({"file": file.filename, "metadata": metadata})
        except HTTPException as e:
            results.append({"file": file.filename, "error": str(e.detail)})
    return results

@app.on_event("shutdown")
def cleanup_temp_dir():
    """Clean up temporary files on shutdown."""
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        logging.info("Temporary directory cleaned up.")
