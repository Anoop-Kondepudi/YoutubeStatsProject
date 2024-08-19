import os
import requests
import zipfile
import subprocess

def get_chrome_version():
    """Get the installed Chrome browser version using PowerShell."""
    try:
        process = subprocess.Popen(
            [
                "powershell",
                "(Get-Item (Get-ItemProperty -Path Registry::'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon').\"version\").VersionInfo.ProductVersion"
            ],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, _ = process.communicate()
        version = out.decode('utf-8').strip()
        return version
    except Exception as e:
        print(f"Error fetching Chrome version: {e}")
        return None

def get_chromedriver_url(version):
    """Get the ChromeDriver download URL based on the Chrome version."""
    base_url = "https://chromedriver.storage.googleapis.com/"
    version_prefix = ".".join(version.split(".")[:3])
    
    # Get the full ChromeDriver version matching the Chrome browser version
    response = requests.get(f"{base_url}LATEST_RELEASE_{version_prefix}")
    if response.status_code == 200:
        full_version = response.text.strip()
        download_url = f"{base_url}{full_version}/chromedriver_win32.zip"
        return download_url
    else:
        print("Failed to get ChromeDriver version.")
        return None

def download_and_extract_chromedriver(url, extract_to="chromedriver"):
    """Download and extract ChromeDriver."""
    zip_path = "chromedriver.zip"
    
    # Download the ChromeDriver zip
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(zip_path, 'wb') as file:
            for chunk in r.iter_content(chunk_size=8192):
                file.write(chunk)

    # Extract the zip
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    
    # Clean up zip file
    os.remove(zip_path)
    print(f"ChromeDriver extracted to: {os.path.abspath(extract_to)}")

def main():
    chrome_version = get_chrome_version()
    if not chrome_version:
        print("Unable to find Chrome version. Make sure Chrome is installed.")
        return
    
    print(f"Installed Chrome version: {chrome_version}")
    download_url = get_chromedriver_url(chrome_version)
    if download_url:
        print(f"Downloading ChromeDriver from: {download_url}")
        download_and_extract_chromedriver(download_url)
    else:
        print("Unable to determine the correct ChromeDriver version to download.")

if __name__ == "__main__":
    main()
