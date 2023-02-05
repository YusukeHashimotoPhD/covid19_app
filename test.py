import requests
import zipfile
import pandas as pd

file_path = 'https://exdeaths-japan.org/data/Observed.csv'
print(pd.read_csv(file_path))
