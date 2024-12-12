import requests

# API Endpoint
url = "http://127.0.0.1:8000/convert"

# Path to the DICOM file
file_path = "D:/My D drive 2024-Oct/MyDevSpace/DICOM-converter-API/testdata/img2.dcm"

# Format to test (change as needed: 'jpeg', 'png', 'pdf', 'tiff', 'mp4')
format_to_test = "mp4"

# Quality for the output (optional, only applies to image formats)
quality = 95

# Make the POST request
try:
    with open(file_path, "rb") as file:
        response = requests.post(
            url,
            files={"file": file},
            data={"format": format_to_test, "quality": quality},
        )

    # Print response details
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Response JSON:", response.json())
    else:
        print("Error:", response.text)
except Exception as e:
    print(f"An error occurred: {e}")
