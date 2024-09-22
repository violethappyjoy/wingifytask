import PyPDF2
import json
import re
from typing import Dict, List, Any


def extract_text_pdf(file_path: str) -> str:
    reader = PyPDF2.PdfReader(file_path)
    text = ""
    for i in range(len(reader.pages)):
        text += reader.pages[i].extract_text()
    return text
