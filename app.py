import streamlit as st
import PyPDF2
import re

st.set_page_config(page_title="PEC CPD Autopilot", layout="centered")
st.title("PEC CPD Autopilot")
st.write("Upload your PEC CPD certificate PDFs to calculate total CPD points")

if "total_points" not in st.session_state:
    st.session_state.total_points = 0.0
    st.session_state.certificates = []

uploaded_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    for uploaded in uploaded_files:
        if uploaded.name in [c['file'] for c in st.session_state.certificates]:
            continue
            
        reader = PyPDF2.PdfReader(uploaded)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        # === AGENT 1: DETECTION AGENT ===
        is_cpd = "CPD" in text.upper() and ("CERTIF" in text.upper() or "PROGRAMME" in text.upper())
        if not is_cpd:
            st.warning(f"❌ {uploaded.name}: Not a CPD Certificate")
            continue
        
        st.success(f"✅ {uploaded.name}: CPD Certificate Found!")

        # === AGENT 2: PARSER / CALCULATOR AGENT ===
        # 1. Points
        points_match = re.search(r'\((\d+(?:\.\d+)?)CPD Point', text)
        points = float(points_match.group(1)) if points_match else 0.0
        
        # 2. Date - handles 19 Sep, 2026 and 26th Sep, 2026 and 19th April, 2026
        date_match = re.search(r'(\d{1,2}(?:th|st|nd|rd)?\s+\w+,\s+\d{4})', text)
        date = date_match.group(1) if date_match else "Not Found"
        
        # 3. Name
        name_match = re.search(r'ENGR\.\s+([A-Z ]+)', text)
        name = name_match.group(0).strip() if name_match else "Not Found"
        
        # 4. REGISTRATION NO - number after name (8241690 / 8245359)
        reg_match = re.search(r'ENGR\.\s+[A-Z ]+\s+(\d{6,})', text)
        reg_no = reg_match.group(1) if reg_match else "Not Found"
        
        # 5. SERIAL NO - top right (8161678)
        serial_match = re.search(r'Serial No:\s*(\d+)', text)
        serial_no = serial_match.group(1) if serial_match else "Not Found"

        # 6. ACTIVITY TITLE - text inside quotes
        title_match = re.search(r'"([^"]+)"', text)
        title = title_match.group(1).strip() if title_match else "CPD Activity"

        st.session_state.certificates.append({
            'file': uploaded.name,
            'points': points,
            'date': date,
            'name': name,
            'reg': reg_no,
            'serial': serial_no,
            'title': title
        })
        st.session_state.total_points += points

        # === DISPLAY CLEAN SUMMARY ===
        st.subheader("📄 CPD Summary")
        col1, col2 = st.columns(2)
        col1.metric("CPD Points", points)
        col2.metric("Date", date)
        st.write(f"**Engineer:** {name}")
        st.write(f"**Reg No:** {reg_no}")
        st.write(f"**Serial No:** {serial_no}")
        st.write(f"**Activity:** {title}")

        with st.expander("Show Full Certificate Text"):
            st.text(text)

# === AGENT 3: VALIDATOR / TOTAL AGENT ===
if st.session_state.certificates:
    st.divider()
    st.subheader("📊 Total CPD Report")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Certificates", len(st.session_state.certificates))
    col2.metric("Total Points", f"{st.session_state.total_points:.1f}")
    
    required = 15.0
    remaining = required - st.session_state.total_points
    if remaining <= 0:
        col3.metric("Status", "✅ Requirement Met")
    else:
        col3.metric("Status", f"Need {remaining:.1f} more")
    
    progress = min(st.session_state.total_points / required, 1.0)
    st.progress(progress)
    st.write(f"Progress: {st.session_state.total_points:.1f} / {required} CPD Points")
    
    st.table(st.session_state.certificates)
    
    if st.button("Reset All"):
        st.session_state.total_points = 0.0
        st.session_state.certificates = []
        st.rerun()
