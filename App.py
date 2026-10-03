import streamlit as st
import PyPDF2
import re

st.set_page_config(page_title="PEC CPD Autopilot")
st.title("PEC CPD Autopilot")
st.write("Upload your PEC CPD certificate PDF")

uploaded = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded:
    reader = PyPDF2.PdfReader(uploaded)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    # Agent 1: Detection
    if "CPD" in text.upper():
        st.success("CPD Certificate Found!")
    else:
        st.warning("No CPD keyword found, check if this is a valid CPD certificate")
        st.stop()

    # Agent 2: Parser / Calculator
    # Points
    match = re.search(r'\((\d+)CPD Point', text)
    points = float(match.group(1)) if match else 0.0
    
    # Date
    date_match = re.search(r'(\d{1,2}th \w+, \d{4})', text)
    date = date_match.group(1) if date_match else "Not found"
    
    # Name
    name_match = re.search(r'ENGR\.\s+([A-Z ]+)', text)
    name = name_match.group(0) if name_match else "Not found"

    # CLEAN SUMMARY (No messy text)
    st.subheader("📄 CPD Summary")
    col1, col2 = st.columns(2)
    col1.metric("CPD Points", points)
    col2.metric("Date", date)
    
    st.write(f"**Engineer:** {name}")

    with st.expander("Show Full Certificate Text (for verification)"):
        st.text(text)
