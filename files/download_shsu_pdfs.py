
import requests
from bs4 import BeautifulSoup
import os

# This is the main policy page
url = 'https://www.shsu.edu/dept/hr/employment/classifications.html'
download_folder = 'shsu_policies'

# Paste your session cookie here (from your browser's DevTools > Application > Cookies)
cookies = {
    'JSESSIONID': 'eyJpZCI6IjU5ZDA4NGJiLTA2NTItNTY5Zi1iNDgzLTEzM2FlYjJhNmZlMyIsImNyZWF0ZWQiOjE3NTE5MTUxNDE4ODMsImV4aXN0aW5nIjp0cnVlfQ=='  # Replace this with your actual session ID
}

headers = {
    'User-Agent': 'Mozilla/5.0'
}

os.makedirs(download_folder, exist_ok=True)

# Get the page
response = requests.get(url, cookies=cookies, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all links to PDFs
for a_tag in soup.find_all('a', href=True):
    href = a_tag['href']
    if href.endswith('.pdf'):
        full_url = href if href.startswith('http') else f'https://www.shsu.edu{href}'
        filename = full_url.split('/')[-1]
        print(f'Downloading: {filename}')
        r = requests.get(full_url, cookies=cookies, headers=headers)
        with open(os.path.join(download_folder, filename), 'wb') as f:
            f.write(r.content)
