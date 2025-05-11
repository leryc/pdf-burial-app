import streamlit as st
import pytesseract
from pdf2image import convert_from_bytes
import re
import subprocess

st.title("📄 PDF OCR Extractor (Render Deployment)")

uploaded_file = st.file_uploader("Upload a scanned PDF", type=["pdf"])

def clean_text(text):
    text = re.sub(r'[~|✓→►•◦■¤©®™¨]', '', text)
    text = re.sub(r'\b(?:J-|SY|v|—|_~|~~|¥|“|”|‘|’|†)\b', '', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

if uploaded_file is not None:
    st.info("⏳ Processing PDF...")
    try:
        # Debug: show tesseract version
        output = subprocess.getoutput("tesseract --version")
        st.text(f"Tesseract version:
{output}")

        images = convert_from_bytes(uploaded_file.read(), dpi=300)
        full_text = ""
        for page in images:
            full_text += pytesseract.image_to_string(page) + "\n"
        cleaned = clean_text(full_text)
        st.success("✅ Text extracted!")
        st.text_area("Extracted Text", cleaned, height=400)
    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
