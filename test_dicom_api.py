import requests
import os

# Define the API Base URL
API_BASE_URL = "http://127.0.0.1:8000"

# Test credentials
USERNAME = "admin"
PASSWORD = "password"

def login():
    """Login to get the JWT token."""
    login_url = f"{API_BASE_URL}/login"
    login_data = {"username": USERNAME, "password": PASSWORD}
    response = requests.post(login_url, data=login_data)  # Use `data` for form fields
    
    if response.status_code == 200:
        print("Login successful!")
        return response.json().get("access_token")
    else:
        print("Login failed:", response.status_code, response.json())
        return None

def test_convert(token, file_path, format, quality):
    """Test the /convert endpoint."""
    url = f"{API_BASE_URL}/convert"
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": open(file_path, "rb")}
    data = {"format": format, "quality": quality}
    
    response = requests.post(url, headers=headers, files=files, data=data)
    
    if response.status_code == 200:
        print("Convert endpoint successful!")
        print("Response:", response.json())
    else:
        print("Convert endpoint failed:", response.status_code, response.json())

def test_convert_batch(token, file_paths, formats, quality):
    """Test the /convert-batch endpoint."""
    url = f"{API_BASE_URL}/convert-batch"
    headers = {"Authorization": f"Bearer {token}"}
    files = [("files", (fp.split("/")[-1], open(fp, "rb"))) for fp in file_paths]
    data = [("formats", fmt) for fmt in formats]
    data.append(("quality", quality))
    
    response = requests.post(url, headers=headers, files=files, data=data)
    
    if response.status_code == 200:
        print("Batch convert endpoint successful!")
        print("Response:", response.json())
    else:
        print("Batch convert endpoint failed:", response.status_code, response.json())

def test_metadata(token, file_path):
    """Test the /metadata endpoint."""
    url = f"{API_BASE_URL}/metadata"
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": open(file_path, "rb")}
    
    response = requests.post(url, headers=headers, files=files)
    
    if response.status_code == 200:
        print("Metadata endpoint successful!")
        print("Response:", response.json())
    else:
        print("Metadata endpoint failed:", response.status_code, response.json())

def test_metadata_batch(token, file_paths):
    """Test the /metadata-batch endpoint."""
    url = f"{API_BASE_URL}/metadata-batch"
    headers = {"Authorization": f"Bearer {token}"}
    files = [("files", (fp.split("/")[-1], open(fp, "rb"))) for fp in file_paths]
    
    response = requests.post(url, headers=headers, files=files)
    
    if response.status_code == 200:
        print("Metadata batch endpoint successful!")
        print("Response:", response.json())
    else:
        print("Metadata batch endpoint failed:", response.status_code, response.json())

def test_convert_to_dicom(token, file_path, input_format, patient_name, patient_id):
    """Test the /convert-to-dicom endpoint."""
    url = f"{API_BASE_URL}/convert-to-dicom"
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": open(file_path, "rb")}
    params = {
        "input_format": input_format,
        "patient_name": patient_name,
        "patient_id": patient_id,
    }
    
    response = requests.post(url, headers=headers, files=files, params=params)
    
    if response.status_code == 200:
        print("Convert-to-DICOM endpoint successful!")
        print("Response:", response.json())
    else:
        print("Convert-to-DICOM endpoint failed:", response.status_code, response.json())


def test_convert_to_dicom_batch(token, file_paths, formats, patient_name, patient_id):
    """Test the /convert-to-dicom-batch endpoint."""
    url = f"{API_BASE_URL}/convert-to-dicom-batch"
    headers = {"Authorization": f"Bearer {token}"}
    
    # Prepare the files
    files = [("files", (os.path.basename(fp), open(fp, "rb"))) for fp in file_paths]
    
    # Prepare query parameters
    params = {
        "input_formats": formats,
        "patient_name": patient_name,
        "patient_id": patient_id
    }
    
    # Send the request
    response = requests.post(url, headers=headers, files=files, params=params)
    
    if response.status_code == 200:
        print("Convert-to-DICOM batch endpoint successful!")
        print("Response:", response.json())
    else:
        print("Convert-to-DICOM batch endpoint failed:", response.status_code, response.json())






if __name__ == "__main__":
    # Login to get the JWT token
    token = login()
    if not token:
        exit("Login failed. Exiting tests.")

    # Define test  - DICOM files
    test_DICOMfile = "D:/My D drive 2024-Oct/MyDevSpace/DICOM-converter-API/testdata/1-001.dcm" # Replace with your DICOM file
    test_DICOMfiles = ["D:/My D drive 2024-Oct/MyDevSpace/DICOM-converter-API/testdata/1-001.dcm", "D:/My D drive 2024-Oct/MyDevSpace/DICOM-converter-API/testdata/1-002.dcm"]  # Replace with multiple file 
    file_MP4File = "D:/My D drive 2024-Oct/MyDevSpace/DICOM-converter-API/testdata/img2.dcm"

    # Non-DICOM files
    testJPEG_file= "D:/My D drive 2024-Oct/MyDevSpace/DICOM-converter-API/testdata/1-001.jpeg"
    testPNG_file= "D:/My D drive 2024-Oct/MyDevSpace/DICOM-converter-API/testdata/1-001.png"
    testPDF_file= "D:/My D drive 2024-Oct/MyDevSpace/DICOM-converter-API/testdata/1-001.pdf"
    testTIFF_file= "D:/My D drive 2024-Oct/MyDevSpace/DICOM-converter-API/testdata/1-001.tiff"
    testMP4_file= "D:/My D drive 2024-Oct/MyDevSpace/DICOM-converter-API/testdata/img2.mp4"

    test_NON_DICOM = [
    "D:/My D drive 2024-Oct/MyDevSpace/DICOM-converter-API/testdata/1-001.jpeg",
    "D:/My D drive 2024-Oct/MyDevSpace/DICOM-converter-API/testdata/1-001.png",
    "D:/My D drive 2024-Oct/MyDevSpace/DICOM-converter-API/testdata/1-001.pdf",
    "D:/My D drive 2024-Oct/MyDevSpace/DICOM-converter-API/testdata/1-001.tiff",
    "D:/My D drive 2024-Oct/MyDevSpace/DICOM-converter-API/testdata/img2.mp4"
]
    


    test_format = "jpeg"
    test_formats = ["jpeg", "png", "pdf", "tiff", "mp4"]
    test_quality = 95
    test_patient_name = "John Doe"
    test_patient_id = "12345"

    # Test single convert endpoint
    print("\nTesting /convert endpoint...")
    #(token, test_file, test_format, test_quality)

    # Test batch convert endpoint
    print("\nTesting /convert-batch endpoint...")
   # test_convert_batch(token, test_files, test_formats, test_quality)

    # Test single metadata endpoint
    print("\nTesting /metadata endpoint...")
    #test_metadata(token, test_file)

    # Test batch metadata endpoint
    print("\nTesting /metadata-batch endpoint...")
    #test_metadata_batch(token, test_files)

    # Test single convert-to-DICOM endpoint
    print("\nTesting /convert-to-dicom endpoint...")
    test_convert_to_dicom(token, testJPEG_file, "jpeg", test_patient_name, test_patient_id)

    # Test batch convert-to-DICOM endpoint
    print("\nTesting /convert-to-dicom-batch endpoint...")
    test_convert_to_dicom_batch(token ,test_NON_DICOM, test_formats, test_patient_name, test_patient_id)
