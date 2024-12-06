# DICOM-converter-API
DICOM converter API



## New Features

Additional Formats

Added support for PNG and GIF.

Added a quality parameter for JPEG and PNG to customize image compression.

Metadata Extraction

Single Metadata Extraction (/metadata):

Extracts metadata from a single DICOM file.

Batch Metadata Extraction (/metadata-batch):

Extracts metadata from multiple DICOM files.

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