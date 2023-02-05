import requests
import zipfile
import pandas as pd

zip_url = 'https://exdeaths-japan.org/data/Observed.csv.zip'
zip_file_path = "example.zip"
extract_to_path = './data/Observed/'

response = requests.get(zip_url)
with open(zip_file_path, "wb") as f:
    f.write(response.content)

with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
    zip_ref.extractall(extract_to_path)
