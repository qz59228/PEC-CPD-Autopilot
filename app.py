import streamlit as st
import PyPDF2

st.set_page_config(page_title="PEC CPD Autopilot", page_icon="")
st.title(" PEC CPD Autopilot")
st.write("Upload your PEC CPD certificate PDF and get points automatically.")

uploaded = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded:
    reader = PyPDF2.PdfReader(uploaded)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    
    st.subheader("Extracted Text:")
    st.text_area("Content", text, height=300)
    
    # Simple CPD points finder
    if "CPD" in text.upper():
        st.success("CPD Certificate Found!")
    else:
        st.warning("No CPD keyword found, check PDF")