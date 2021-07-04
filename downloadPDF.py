from pathlib import Path
import requests


def savePDF(url):
    filename = Path('resume.pdf')
    response = requests.get(url)
    filename.write_bytes(response.content)