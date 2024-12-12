import requests

# Define the API endpoint
API_URL = "http://127.0.0.1:8000/convert-to-dicom-batch"

# Define the files to upload
files = [
    ("files", ("1-001.jpeg", open("D:/My D drive 2024-Oct/MyDevSpace/DICOM-converter-API/testdata/1-001.jpeg", "rb"), "image/jpeg")),
    ("files", ("1-002.pdf", open("D:/My D drive 2024-Oct/MyDevSpace/DICOM-converter-API/testdata/1-002.pdf", "rb"), "application/pdf"))
]

# Define the query parameters
params = {
    "input_formats": ["jpeg", "pdf"],
    "patient_name": "John Doe",
    "patient_id": "12345"
}

# Send the POST request
response = requests.post(API_URL, files=files, params=params)

# Handle the response
if response.status_code == 200:
    print("Batch Conversion Results:")
    print(response.json())
else:
    print("Error:", response.status_code, response.json())
