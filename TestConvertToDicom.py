import requests

# Define the API endpoint
API_URL = "http://127.0.0.1:8000/convert-to-dicom"

# Define the file path and metadata
file_path = "D:/My D drive 2024-Oct/MyDevSpace/DICOM-converter-API/testdata/img2.mp4"  # Replace with the actual file path
input_format = "mp4"  # Change to the format of your file (e.g., 'pdf', 'tiff', etc.)
patient_name = "John Doe"
patient_id = "12345"

# Prepare the request data
try:
    with open(file_path, "rb") as f:
        files = {"file": f}

        # Append query parameters to the URL
        params = {
            "input_format": input_format,
            "patient_name": patient_name,
            "patient_id": patient_id,
        }

        # Send the request to the API
        response = requests.post(API_URL, files=files, params=params)

        # Check the response status
        if response.status_code == 200:
            print("Conversion Successful!")
            print("DICOM File Path:", response.json().get("file_path"))
        else:
            print("Conversion Failed!")
            print("Status Code:", response.status_code)
            print("Error Message:", response.json())
except FileNotFoundError:
    print(f"File not found: {file_path}")
except Exception as e:
    print("An error occurred while testing the endpoint:", str(e))
