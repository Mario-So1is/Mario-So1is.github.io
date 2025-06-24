import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import zipfile

# Base configuration
start_url = "https://www.shsu.edu/dept/hr/"
domain = "www.shsu.edu"
download_folder = "shsu_policies"
zip_filename = "shsu_policies.zip"
file_types = [".pdf", ".docx"]

visited_urls = set()

# Create folder to store downloads
os.makedirs(download_folder, exist_ok=True)

def download_file(file_url):
    filename = os.path.join(download_folder, file_url.split("/")[-1])
    if not os.path.exists(filename):
        print(f"Downloading: {file_url}")
        try:
            r = requests.get(file_url, timeout=10)
            with open(filename, "wb") as f:
                f.write(r.content)
        except Exception as e:
            print(f"Error downloading {file_url}: {e}")
    else:
        print(f"Already downloaded: {file_url}")

def crawl(url):
    if url in visited_urls:
        return
    visited_urls.add(url)

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return

    for link in soup.find_all("a", href=True):
        href = link["href"]
        full_url = urljoin(url, href)
        parsed = urlparse(full_url)

        # Ensure the link is on shsu.edu
        if domain in parsed.netloc:
            if any(full_url.lower().endswith(ext) for ext in file_types):
                download_file(full_url)
            elif full_url not in visited_urls:
                crawl(full_url)

def zip_downloads():
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(download_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, download_folder)
                zipf.write(file_path, arcname)
    print(f"\n✅ All files zipped into: {zip_filename}")

# Run everything
crawl(start_url)
zip_downloads()
