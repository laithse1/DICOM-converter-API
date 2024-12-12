from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Request
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
import numpy as np
from pdf2image import convert_from_path
from pydicom.uid import ExplicitVRLittleEndian , generate_uid
from pydicom.dataset import Dataset
from pdf2image import convert_from_path



# Configure logging
logging.basicConfig(
    filename="dicom_converter.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Initialize FastAPI app
app = FastAPI(
    title="Enhanced DICOM Converter API",
    description="API to convert DICOM files to various formats and extract metadata."
)

# Temporary directory for file processing
temp_dir = tempfile.mkdtemp()

# Helper Functions


def decode_pixel_data(dicom):
    """Decode pixel data, handling compressed formats correctly."""
    try:
        dicom.decode()  # Ensure compressed data is decoded
        pixel_array = apply_voi_lut(dicom.pixel_array, dicom)

        # Handle floating-point pixel data
        if pixel_array.dtype.kind == 'f':  # Check if dtype is floating-point
            pixel_array = (255 * (pixel_array - np.min(pixel_array)) / (np.max(pixel_array) - np.min(pixel_array))).astype(np.uint8)

        # Handle YBR_FULL_422 photometric interpretation
        if dicom.PhotometricInterpretation == 'YBR_FULL_422':
            return Image.fromarray(pixel_array, mode='YCbCr').convert('RGB')
        else:
            return Image.fromarray(pixel_array)
    except Exception as e:
        logging.error(f"Error decoding pixel data: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to decode pixel data.")


def dicom_to_format(dicom_file: UploadFile, output_folder: str, format: str, quality: int = 95) -> str:
    """Convert DICOM to the specified format."""
    try:
        # Save uploaded DICOM file temporarily
        input_path = os.path.join(output_folder, dicom_file.filename)
        with open(input_path, "wb") as f:
            shutil.copyfileobj(dicom_file.file, f)

        # Read DICOM file
        dicom = pydicom.dcmread(input_path, force=True)
        pixel_array = apply_voi_lut(dicom.pixel_array, dicom)

        # Normalize floating-point data if applicable
        if pixel_array.dtype.kind == 'f':
            pixel_array = (255 * (pixel_array - np.min(pixel_array)) / (np.max(pixel_array) - np.min(pixel_array))).astype(np.uint8)

        # Log the requested format
        logging.info(f"Converting {dicom_file.filename} to {format.upper()}")

        # Handle conversions
        if format in ["jpeg", "png"]:
            image = decode_pixel_data(dicom)
            output_path = os.path.join(output_folder, dicom_file.filename.replace(".dcm", f".{format}"))
            image.save(output_path, format.upper(), quality=quality)

        elif format == "pdf":
            image = decode_pixel_data(dicom)
            output_path = os.path.join(output_folder, dicom_file.filename.replace(".dcm", ".pdf"))
            pdf = canvas.Canvas(output_path)
            metadata = f"Patient Name: {dicom.get('PatientName', 'Unknown')}\nStudy Date: {dicom.get('StudyDate', 'Unknown')}\n"
            pdf.drawString(50, 800, metadata)

            # Temporary image for embedding in PDF
            temp_image_path = os.path.join(output_folder, "temp_image.jpg")
            image.save(temp_image_path, "JPEG")
            pdf.drawImage(temp_image_path, 50, 600, width=500, height=500)
            pdf.save()
            os.remove(temp_image_path)

        elif format == "tiff":
            output_path = os.path.join(output_folder, dicom_file.filename.replace(".dcm", ".tiff"))
            imwrite(output_path, pixel_array)

        elif format == "mp4":
            if len(pixel_array.shape) < 3 or pixel_array.shape[0] < 2:
                raise HTTPException(status_code=400, detail="MP4 conversion requires multi-frame DICOM files.")

            output_path = os.path.join(output_folder, dicom_file.filename.replace(".dcm", ".mp4"))
            height, width = pixel_array[0].shape
            video_writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), 10, (width, height))
            for frame in pixel_array:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
                video_writer.write(rgb_frame)
            video_writer.release()

        else:
            logging.error(f"Unsupported format: {format}")
            raise HTTPException(status_code=400, detail=f"Unsupported format: {format}")

        logging.info(f"Successfully converted {dicom_file.filename} to {format.upper()} at {output_path}")
        return output_path

    except Exception as e:
        logging.error(f"Error converting {dicom_file.filename} to {format.upper()}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to convert DICOM to {format.upper()}.")
    

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

# API Endpoints


@app.post("/convert", response_class=JSONResponse)
async def convert_dicom(
    request: Request,
    file: UploadFile = File(...),
    quality: int = Query(95)
):
    """Convert a single DICOM file to the specified format."""
    # Extract form data
    form_data = await request.form()
    logging.info(f"Raw Request Data: {form_data}")

    # Extract `format` from form data
    format = form_data.get("format", "jpeg")  # Default to "jpeg" if not provided
    logging.info(f"Format extracted from form data: '{format}', Quality received: '{quality}'")

    # Validate the format
    supported_formats = ["jpeg", "png", "pdf", "tiff", "mp4"]
    if format not in supported_formats:
        logging.error(f"Unsupported format requested: {format}")
        raise HTTPException(status_code=400, detail=f"Unsupported format: {format}")

    # Proceed with conversion
    logging.info(f"Calling dicom_to_format with format: {format.upper()}")
    output_path = dicom_to_format(file, temp_dir, format, quality)
    logging.info(f"Conversion successful: {file.filename} to {format.upper()} at {output_path}")
    return {"file_path": output_path}


# Additional endpoints like batch conversion and metadata...

@app.post("/convert-batch", response_model=List[dict])
async def batch_convert_dicom(request: Request, files: List[UploadFile] = File(...), quality: int = 95):
    """Batch convert multiple DICOM files to multiple formats."""
    # Extract form data
    form_data = await request.form()
    logging.info(f"Raw Request Data: {form_data}")

    # Extract formats from form data
    formats = form_data.getlist("formats")  # Get list of formats
    if not formats:
        formats = ["jpeg"]  # Default to "jpeg" if not provided
    logging.info(f"Formats extracted from form data: {formats}")

    # Validate formats
    supported_formats = ["jpeg", "png", "pdf", "tiff", "mp4"]
    invalid_formats = [fmt for fmt in formats if fmt not in supported_formats]
    if invalid_formats:
        logging.error(f"Unsupported formats requested: {invalid_formats}")
        raise HTTPException(status_code=400, detail=f"Unsupported formats: {invalid_formats}")

    # Process each file for the requested formats
    results = []
    for file in files:
        file_results = {"input_file": file.filename, "outputs": []}
        for format in formats:
            try:
                # Reset file pointer to ensure fresh read
                file.file.seek(0)

                # Convert the file to the specified format
                output_path = dicom_to_format(file, temp_dir, format, quality)

                # Append success result
                file_results["outputs"].append({
                    "format": format,
                    "file_path": output_path,
                    "status": "success"
                })
            except HTTPException as e:
                # Capture FastAPI-specific errors
                error_message = f"Error converting to {format.upper()}: {str(e.detail)}"
                logging.error(error_message)
                file_results["outputs"].append({
                    "format": format,
                    "status": "failed",
                    "error": error_message
                })
            except Exception as e:
                # Capture unexpected errors
                error_message = f"Unexpected error during {format.upper()} conversion: {str(e)}"
                logging.error(error_message)
                file_results["outputs"].append({
                    "format": format,
                    "status": "failed",
                    "error": error_message
                })

        results.append(file_results)

    logging.info(f"Batch conversion completed with results: {results}")
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



# Other formats ["jpeg", "pdf", "tiff", "png", "mp4"] to DICOM:


def convert_image_to_dicom(input_path, output_path, patient_name, patient_id):
    """Convert an image (jpeg, png, tiff) to a DICOM file."""
    try:
        image = Image.open(input_path).convert("L")  # Convert to grayscale
        pixel_array = np.array(image)

        # Create a DICOM dataset
        dicom = Dataset()
        dicom.PatientName = patient_name
        dicom.PatientID = patient_id

        # Set the Transfer Syntax UID (mandatory for DICOM files)
        dicom.file_meta = Dataset()
        dicom.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

        # Add pixel data
        dicom.Rows, dicom.Columns = pixel_array.shape
        dicom.PixelData = pixel_array.tobytes()
        dicom.SamplesPerPixel = 1
        dicom.PhotometricInterpretation = "MONOCHROME2"
        dicom.BitsAllocated = 8
        dicom.BitsStored = 8
        dicom.HighBit = 7
        dicom.PixelRepresentation = 0

        # Save as DICOM
        dicom.save_as(output_path)
        logging.info(f"Successfully converted image {input_path} to DICOM {output_path}")
    except Exception as e:
        logging.error(f"Error converting image {input_path} to DICOM: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error converting {os.path.basename(input_path)} to DICOM: {str(e)}"
        )



def convert_pdf_to_dicom(input_path, output_path, patient_name, patient_id):
    """Convert a PDF file to a DICOM file."""
    try:
        # Convert PDF to images
        images = convert_from_path(input_path)
        if not images:
            raise Exception("No pages found in the PDF.")

        # Take the first page as the image
        image = images[0].convert("L")  # Convert to grayscale
        pixel_array = np.array(image)

        # Create a DICOM dataset
        dicom = Dataset()
        dicom.PatientName = patient_name
        dicom.PatientID = patient_id

        # Set the Transfer Syntax UID (mandatory for DICOM files)
        dicom.file_meta = Dataset()
        dicom.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

        # Add pixel data
        dicom.Rows, dicom.Columns = pixel_array.shape
        dicom.PixelData = pixel_array.tobytes()
        dicom.SamplesPerPixel = 1
        dicom.PhotometricInterpretation = "MONOCHROME2"
        dicom.BitsAllocated = 8
        dicom.BitsStored = 8
        dicom.HighBit = 7
        dicom.PixelRepresentation = 0

        # Save as DICOM
        dicom.save_as(output_path)
        logging.info(f"Successfully converted PDF {input_path} to DICOM {output_path}")

    except FileNotFoundError:
        logging.error("Poppler is not installed or not in PATH.")
        raise HTTPException(
            status_code=500,
            detail="PDF conversion requires Poppler. Please ensure it is installed and added to PATH."
        )
    except Exception as e:
        logging.error(f"Error converting PDF {input_path} to DICOM: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error converting {os.path.basename(input_path)} to DICOM: {str(e)}"
        )


def convert_video_to_dicom(input_path, output_path, patient_name, patient_id):
    """Convert a video file (e.g., MP4) to a DICOM file."""
    try:
        # Open the video file using OpenCV
        video_capture = cv2.VideoCapture(input_path)
        frames = []

        # Read video frames
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frames.append(gray_frame)

        if not frames:
            raise Exception("No frames extracted from the video.")

        # Create a DICOM dataset
        dicom = Dataset()
        dicom.PatientName = patient_name
        dicom.PatientID = patient_id

        # Set the Transfer Syntax UID (mandatory for DICOM files)
        dicom.file_meta = Dataset()
        dicom.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
        dicom.file_meta.MediaStorageSOPClassUID = generate_uid()
        dicom.file_meta.MediaStorageSOPInstanceUID = generate_uid()
        dicom.file_meta.ImplementationClassUID = generate_uid()

        # Add pixel data for all frames
        pixel_array = np.stack(frames, axis=0)  # Stack frames into a 3D array
        dicom.Rows, dicom.Columns = pixel_array.shape[1], pixel_array.shape[2]
        dicom.NumberOfFrames = len(frames)
        dicom.PixelData = pixel_array.tobytes()
        dicom.SamplesPerPixel = 1
        dicom.PhotometricInterpretation = "MONOCHROME2"
        dicom.BitsAllocated = 8
        dicom.BitsStored = 8
        dicom.HighBit = 7
        dicom.PixelRepresentation = 0

        # Save as DICOM
        dicom.save_as(output_path)
        video_capture.release()

        logging.info(f"Successfully converted video {input_path} to DICOM {output_path}")
    except FileNotFoundError:
        logging.error("Video file not found.")
        raise HTTPException(
            status_code=404,
            detail="Video file not found."
        )
    except Exception as e:
        logging.error(f"Error converting video {input_path} to DICOM: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error converting video to DICOM: {str(e)}"
        )







@app.post("/convert-to-dicom", response_class=JSONResponse)
async def convert_to_dicom(
    file: UploadFile = File(...),
    input_format: str = Query(...),
    patient_name: str = Query("Anonymous"),
    patient_id: str = Query("000000")
):
    try:
        temp_input_path = os.path.join(temp_dir, file.filename)
        with open(temp_input_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        output_dicom_path = os.path.join(temp_dir, file.filename.replace(f".{input_format}", ".dcm"))

        if input_format in ["jpeg", "png", "tiff"]:
            convert_image_to_dicom(temp_input_path, output_dicom_path, patient_name, patient_id)
        elif input_format == "pdf":
            convert_pdf_to_dicom(temp_input_path, output_dicom_path, patient_name, patient_id)
        elif input_format == "mp4":
            convert_video_to_dicom(temp_input_path, output_dicom_path, patient_name, patient_id)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported input format: {input_format}")

        return {"file_path": output_dicom_path}
    except HTTPException as e:
        # Pass through HTTP exceptions
        logging.error(f"HTTP Error: {str(e)}")
        raise e
    except Exception as e:
        # Catch-all for unexpected exceptions
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")




@app.post("/convert-to-dicom-batch", response_model=List[dict])
async def batch_convert_to_dicom(
    files: List[UploadFile] = File(...),
    input_formats: List[str] = Query(..., description="Input formats corresponding to each file (e.g., jpeg, png, pdf, tiff, mp4)"),
    patient_name: str = Query("Anonymous"),
    patient_id: str = Query("000000")
):
    """
    Batch convert multiple files into DICOM format.
    """
    results = []
    if len(files) != len(input_formats):
        raise HTTPException(
            status_code=400,
            detail="The number of files and input formats must match."
        )

    for file, input_format in zip(files, input_formats):
        file_result = {
            "input_file": file.filename,
            "input_format": input_format,
            "status": "pending",
            "output_file": None,
            "error": None
        }

        try:
            # Save the uploaded file temporarily
            temp_input_path = os.path.join(temp_dir, file.filename)
            with open(temp_input_path, "wb") as f:
                shutil.copyfileobj(file.file, f)

            # Define the output DICOM file path
            output_dicom_path = os.path.join(temp_dir, file.filename.replace(f".{input_format}", ".dcm"))

            # Call the appropriate conversion function based on format
            if input_format in ["jpeg", "png", "tiff"]:
                convert_image_to_dicom(temp_input_path, output_dicom_path, patient_name, patient_id)
            elif input_format == "pdf":
                convert_pdf_to_dicom(temp_input_path, output_dicom_path, patient_name, patient_id)
            elif input_format == "mp4":
                convert_video_to_dicom(temp_input_path, output_dicom_path, patient_name, patient_id)
            else:
                raise HTTPException(status_code=400, detail=f"Unsupported input format: {input_format}")

            # Update result on success
            file_result["status"] = "success"
            file_result["output_file"] = output_dicom_path
        except HTTPException as e:
            # Update result on HTTP exception
            file_result["status"] = "failed"
            file_result["error"] = e.detail
        except Exception as e:
            # Update result on general exception
            file_result["status"] = "failed"
            file_result["error"] = str(e)

        results.append(file_result)

    return results


# Temp folder cleanup

@app.on_event("shutdown")
def cleanup_temp_dir():
    """Clean up temporary files on shutdown."""
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        logging.info("Temporary directory cleaned up.")
