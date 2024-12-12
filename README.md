# DICOM-converter-API
### **DICOM Converter API: Summary**

The **DICOM Converter API** is a robust solution for handling medical imaging data, enabling seamless conversion between various formats and the DICOM standard. Built with FastAPI, it is designed to be efficient, scalable, and user-friendly for healthcare and imaging workflows.

---

### **Features**

#### **1. Format Conversion**
- **From DICOM**:
  - Convert DICOM files into widely-used formats:
    - **JPEG**: Single-frame images.
    - **PNG**: High-quality single-frame images.
    - **PDF**: Embedded metadata and image data.
    - **TIFF**: Multi-frame high-resolution images.
    - **MP4**: Multi-frame sequences as video files.

- **To DICOM**:
  - Convert various formats into DICOM:
    - **JPEG**: Single-frame DICOM.
    - **PNG**: Single-frame DICOM.
    - **PDF**: PDF pages converted to multi-frame DICOM.
    - **TIFF**: Multi-frame DICOM.
    - **MP4**: Videos converted into multi-frame DICOM.

---

#### **2. Metadata Extraction**
- Extract detailed metadata from DICOM files, including:
  - Patient Name
  - Patient ID
  - Study Date
  - Modality
  - Study Description
  - Manufacturer

---

#### **3. Batch Processing**
- Process multiple files in a single API request:
  - Convert multiple files to desired formats (e.g., DICOM, JPEG, TIFF).
  - Handle errors gracefully for individual files without interrupting the batch process.

---

#### **4. Robust Error Handling**
- Comprehensive error reporting for API consumers:
  - Clearly indicate failures for individual files in batch operations.
  - Include detailed messages about missing files, unsupported formats, or conversion issues.

---

### **Endpoints**

#### **1. `/convert`**
- **Purpose**: Convert a single DICOM file to various formats.
- **Input**: File, target format, and optional quality parameter.
- **Output**: Converted file path.

#### **2. `/convert-batch`**
- **Purpose**: Convert multiple DICOM files to multiple formats.
- **Input**: List of files and target formats.
- **Output**: Conversion results for each file and format.

#### **3. `/convert-to-dicom`**
- **Purpose**: Convert supported formats (JPEG, PNG, PDF, TIFF, MP4) into DICOM.
- **Input**: File, input format, and metadata (e.g., Patient Name, ID).
- **Output**: Generated DICOM file path.

#### **4. `/convert-to-dicom-batch`**
- **Purpose**: Batch conversion of multiple files into DICOM.
- **Input**: List of files, input formats, and metadata.
- **Output**: Conversion results for each file.

#### **5. `/metadata`**
- **Purpose**: Extract metadata from a single DICOM file.
- **Input**: File.
- **Output**: Metadata as a JSON object.

#### **6. `/metadata-batch`**
- **Purpose**: Extract metadata from multiple DICOM files.
- **Input**: List of files.
- **Output**: Metadata for each file.

---

### **Technical Highlights**
1. **Built with FastAPI**:
   - High performance and modern Python capabilities.
   - Interactive API documentation via Swagger and ReDoc.

2. **Advanced Conversion Logic**:
   - Leverages libraries like `pydicom`, `Pillow`, `opencv-python`, `pdf2image`, and `tifffile`.

3. **Batch Error Resilience**:
   - Handles failures on a per-file basis in batch operations.
   - Provides detailed logs and structured error responses.

4. **Extensibility**:
   - Easily add support for more formats or advanced metadata extraction.

---

### **Use Cases**
1. **Healthcare Providers**:
   - Manage and exchange medical images in DICOM format across systems.
   - Convert DICOM files into formats for presentations or reports.

2. **Research and Development**:
   - Process and analyze large datasets of imaging files.
   - Automate format conversions for AI/ML pipelines.

3. **Imaging Centers**:
   - Create DICOM files from scanned documents or patient data.

---

### **Quick Setup**
1. Clone the repository.
2. Install dependencies (`pip install -r requirements.txt`).
3. Run the API locally or as a Docker container.
4. Access the interactive API documentation at `/docs`.

---




## New Features

- Added a quality parameter for JPEG and PNG to customize image compression.

- Metadata Extraction.

- Single Metadata Extraction (/metadata):

- Extracts metadata from a single DICOM file.

- Batch Metadata Extraction (/metadata-batch):

- Extracts metadata from multiple DICOM files.

## Endpoints
Convert a Single File

URL: /convert

## Parameters:
file: DICOM file to convert.

format: Output format (jpeg, png, gif, mp4, pdf, tiff).

quality: Optional quality setting for JPEG/PNG (default: 95).

Batch Conversion

URL: /convert-batch

## Parameters:
files: List of DICOM files.

formats: List of output formats (e.g., ["jpeg", "pdf"]).

quality: Optional quality setting for JPEG/PNG.

Single Metadata Extraction

URL: /metadata

## Parameters:
file: DICOM file.

Batch Metadata Extraction

URL: /metadata-batch

## Parameters:
files: List of DICOM files.


Example API Calls
Extract Metadata for a Single File:

```
curl -X POST "http://127.0.0.1:8000/metadata" \
-F "file=@example.dcm"

```
Batch Metadata Extraction:

```
curl -X POST "http://127.0.0.1:8000/metadata-batch" \
-F "files=@example1.dcm" \
-F "files=@example2.dcm"

```

Batch Conversion to PNG and PDF:

```
curl -X POST "http://127.0.0.1:8000/convert-batch" \
-F "files=@example1.dcm" \
-F "files=@example2.dcm" \
-F "formats=png" \
-F "formats=pdf"
```



Step 1: Activate the Virtual Environment
Ensure your virtual environment is activated. If you see (venv) or similar in your terminal, it’s active. If not, activate it:

For Windows:

```
.venv\Scripts\activate
```
For Mac/Linux:

```
source .venv/bin/activate

```

Step 2: Install FastAPI
Install FastAPI in the active virtual environment using pip:

```
pip install fastapi

```
Verify Installation:
Run the following to check if FastAPI is installed:

```
pip show fastapi

```

You should see details like version and location if it's installed.


Step 1: Install Uvicorn
Make sure you have uvicorn installed in your Python environment.

Install via pip:
Run the following command in your terminal or PowerShell:

```
pip install uvicorn

```
Verify Installation:
Check if uvicorn is installed by running:

```
uvicorn --version
```
If this command outputs a version, uvicorn is installed correctly.


The error indicates that the FastAPI module is not installed in your Python environment. Follow these steps to resolve the issue:

Step 1: Activate the Virtual Environment

Ensure your virtual environment is activated. If you see (venv) or similar in your terminal, it’s active. 

If not, activate it:

For Windows:
```
.venv\Scripts\activate

```
For Mac/Linux:

```
source .venv/bin/activate
```
Step 2: Install FastAPI
Install FastAPI in the active virtual environment using pip:

```
pip install fastapi

```
Verify Installation:
Run the following to check if FastAPI is installed:

```
pip show fastapi

```
You should see details like version and location if it's installed.

Step 3: Install ASGI Server (Uvicorn)
FastAPI requires an ASGI server like Uvicorn to run. If it’s not already installed, run:

```
pip install uvicorn

```

Step 4: Run the API
After installing FastAPI and Uvicorn, start the API:

```
python -m uvicorn dicom_converter_api:app --reload

```


Install Missing Dependencies in Bulk

```
pip install fastapi uvicorn pydicom pillow numpy opencv-python-headless tifffile reportlab pylibjpeg pylibjpeg-libjpeg pylibjpeg-openjpeg

```


----------------------------------------------------------------

1. Built-in Interactive Documentation

FastAPI provides Swagger UI and ReDoc for interactive API testing.

Access the API Documentation:

Start the API: 

Run the API locally:

```
uvicorn dicom_converter_api:app --reload

```
Open Swagger UI:

Visit http://127.0.0.1:8000/docs.

This interface allows you to test all endpoints interactively by uploading files and providing parameters.
Open ReDoc:

Visit http://127.0.0.1:8000/redoc.

This provides a detailed view of the API structure.

2. Testing with curl

You can use the curl command to test each endpoint from the command line. Below are example commands for all endpoints:

Single File Conversion
Convert a DICOM file to JPEG:

```
curl -X POST "http://127.0.0.1:8000/convert" \
-F "file=@path/to/example.dcm" \
-F "format=jpeg"

```
Convert a DICOM file to PDF:

```
curl -X POST "http://127.0.0.1:8000/convert" \
-F "file=@path/to/example.dcm" \
-F "format=pdf"

```
Batch Conversion
Convert multiple DICOM files to PNG and TIFF:

```
curl -X POST "http://127.0.0.1:8000/convert-batch" \
-F "files=@path/to/example1.dcm" \
-F "files=@path/to/example2.dcm" \
-F "formats=png" \
-F "formats=tiff"

```

Single Metadata Extraction
Extract metadata from a single DICOM file:

```
curl -X POST "http://127.0.0.1:8000/metadata" \
-F "file=@path/to/example.dcm"
```

Batch Metadata Extraction
Extract metadata from multiple DICOM files:

```
curl -X POST "http://127.0.0.1:8000/metadata-batch" \
-F "files=@path/to/example1.dcm" \
-F "files=@path/to/example2.dcm"

```

3. Testing with Postman

Postman provides a user-friendly interface to test REST APIs.

Steps:

Download Postman: Install it from https://www.postman.com/.

Create a New Request:

Select POST as the HTTP method.

Enter the endpoint URL, e.g., http://127.0.0.1:8000/convert.

Add Parameters:

For file uploads:

Go to the Body tab, select form-data, and add a file field to upload the DICOM file.

Add other fields like format and quality as required.

Send Request:

Click Send to see the response.

4. Automated Testing with pytest

Install Required Libraries

Install pytest and httpx:

```
pip install pytest httpx

```
Write Test Cases

Create a file named test_api.py in the same directory as your API code and write the following test cases:

```

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_single_conversion():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        with open("path/to/example.dcm", "rb") as file:
            response = await client.post(
                "/convert",
                files={"file": file},
                data={"format": "jpeg"}
            )
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_batch_conversion():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        files = [
            ("files", ("example1.dcm", open("path/to/example1.dcm", "rb"), "application/dicom")),
            ("files", ("example2.dcm", open("path/to/example2.dcm", "rb"), "application/dicom"))
        ]
        response = await client.post(
            "/convert-batch",
            files=files,
            data={"formats": ["jpeg", "pdf"]}
        )
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_metadata_extraction():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as client:
        with open("path/to/example.dcm", "rb") as file:
            response = await client.post(
                "/metadata",
                files={"file": file}
            )
        assert response.status_code == 200
        assert "PatientName" in response.json()

````

Run Tests
Execute the test cases using:

```
pytest test_api.py

```

5. Verifying Outputs
After testing the API, check the outputs:

Converted Files: Outputs will be saved in the temporary directory (temp_dir).

Verify that the converted files (e.g., .jpeg, .mp4, .pdf) are correct.

Metadata Responses:

Ensure the extracted metadata matches the expected DICOM file contents.

6. Debugging Tips

Check logs in the terminal or the configured log file (logging).

If an endpoint fails, verify:

The DICOM file format is valid.

The file contains the required data (e.g., pixel data for image generation).

## Run the following command to build the Docker image:

```
docker build -t dicom-api .
```

This creates a Docker image named dicom-api

## Run the container and expose the API to the host:

```
docker run -d --name dicom-api -p 8000:8000 dicom-api
```
-d: Runs the container in detached mode (background).

--name: Names the container dicom-api.

-p 8000:8000: Maps the container's port 8000 to the host's port 8000.

For easier management, create a docker-compose.yml file:

Run the application with:

```
docker-compose up -d

```

## Persistent Logs

Mount a volume to save logs outside the container:

```
docker run -d --name dicom-api -p 8000:8000 -v /var/log/dicom-api:/app/logs dicom-api

```

## Monitor Containers
Use Docker commands to manage and monitor:

Check running containers:

```
docker ps
```
View logs:

```
docker logs dicom-api

```
Here’s a list of all the required libraries for this API to run, including their purpose and installation commands:

Core Libraries

1.	fastapi:

o	Used to create the API framework.

o	Installation: 

o	pip install fastapi

2.	uvicorn:

o	ASGI server to run the FastAPI app.

o	Installation: 

o	pip install uvicorn

3.	typing:


o	Provides type annotations (part of Python standard library in Python 3.5+).

4.	os, shutil, tempfile:

o	Standard Python libraries for file system operations.

________________________________________
DICOM Handling

5.	pydicom: 

o	Used to handle DICOM file operations.

o	Installation: 

o	pip install pydicom

________________________________________
Image and Video Processing

6.	Pillow:

o	Used for image processing (e.g., JPEG, PNG, TIFF).

o	Installation: 

o	pip install pillow

7.	opencv-python:

o	Used for video processing (e.g., MP4).

o	Installation: 

o	pip install opencv-python

8.	numpy:

o	Used for handling pixel data and numerical operations.

o	Installation: 

o	pip install numpy

________________________________________
PDF Handling

9.	reportlab:

o	Used to create PDF files.

o	Installation: 

o	pip install reportlab

10.	pdf2image:

o	Used to convert PDF pages to images.

o	Installation:

o	pip install pdf2image

o	Additional Dependency: Requires poppler-utils (see below).
________________________________________
TIFF Handling

11.	tifffile: 

o	Used to handle TIFF image files.

o	Installation: 

o	pip install tifffile

________________________________________
External Dependency

12.	poppler-utils: 

o	Required for pdf2image to work.

o	Installation: 

	Ubuntu/Debian: 

	sudo apt install poppler-utils

	MacOS: 

	brew install poppler

	Windows: 

	Download the Poppler binary from Poppler for Windows.

	Add the bin folder to your system's PATH.

________________________________________
Install All Dependencies at Once

To simplify, create a requirements.txt file with the following contents:

fastapi

uvicorn

pydicom

pillow

opencv-python

numpy

reportlab

pdf2image

tifffile

Then, install all dependencies using:

pip install -r requirements.txt

For poppler-utils, ensure it is installed separately as per the instructions above.
________________________________________
Verify Installations

After installing, verify by running:

python -c "import fastapi, pydicom, PIL, cv2, numpy, reportlab, tifffile, pdf2image; print('All libraries installed successfully!')"




Here is the complete list of required libraries for the DICOM Converter API to function correctly:
________________________________________
Required Libraries

Python Libraries (Installable via pip)
1.	FastAPI

o	Web framework for building APIs.

o	Install: 

o	pip install fastapi

2.	Uvicorn

o	ASGI server to run FastAPI.

o	Install: 

o	pip install uvicorn

3.	Pillow

o	Library for image processing (used for JPEG, PNG, TIFF handling).

o	Install: 

o	pip install pillow

4.	pydicom

o	Library to handle DICOM files (reading, writing, and processing).

o	Install: 

o	pip install pydicom

5.	tifffile

o	Library for reading and writing TIFF files.

o	Install: 

o	pip install tifffile

6.	numpy

o	Numerical computing library (used for pixel data manipulation).

o	Install: 

o	pip install numpy

7.	opencv-python

o	Library for video processing (used for MP4 to DICOM conversion).

o	Install: 

o	pip install opencv-python

8.	pdf2image

o	Library to convert PDF pages to images (requires Poppler installed).

o	Install: 

o	pip install pdf2image

9.	reportlab

o	Library for generating PDFs (used for embedding DICOM metadata in PDFs).

o	Install: 

o	pip install reportlab

10.	typing-extensions

o	Provides additional type hints and utilities for type checking.

o	Install: 

o	pip install typing-extensions

Poppler

•	Required by pdf2image for PDF processing.

•	Install manually on your system: 

o	Windows: Download Poppler for Windows, extract, and add to PATH.

o	Linux: 

o	sudo apt install poppler-utils

o	MacOS: 

o	brew install poppler
________________________________________
Optional for Development

1.	Requests

o	HTTP client for testing endpoints.

o	Install: 

o	pip install requests

2.	Python-dotenv

o	Manage environment variables from a .env file (if used).

o	Install: 

o	pip install python-dotenv

________________________________________
Full Installation Command

You can install all required Python libraries in one command:

pip install fastapi uvicorn pillow pydicom tifffile numpy opencv-python pdf2image reportlab typing-extensions

________________________________________
System Requirements

•	Poppler: Must be installed and accessible in the system PATH for PDF conversion.

•	Python Version: Ensure Python 3.8 or higher.

________________________________________





















