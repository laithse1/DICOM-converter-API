import requests

# Batch Conversion Test
batch_url = "http://127.0.0.1:8000/convert-batch"

# List of DICOM files for batch testing
dicom_files = ["D:/My D drive 2024-Oct/MyDevSpace/DICOM-converter-API/testdata/1-001.dcm", "D:/My D drive 2024-Oct/MyDevSpace/DICOM-converter-API/testdata/1-002.dcm"]

# Formats to test
formats_to_test = ["jpeg", "pdf", "tiff", "png", "mp4"]

# Create the request payload
files = [("files", (open(f, "rb"))) for f in dicom_files]
data = {"formats": formats_to_test, "quality": 95}

# Make the POST request
try:
    response = requests.post(batch_url, files=files, data=data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Response JSON:", response.json())
    else:
        print("Error:", response.text)
except Exception as e:
    print(f"An error occurred: {e}")
