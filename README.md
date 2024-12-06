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