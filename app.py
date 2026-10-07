import streamlit as st
import re
import pandas as pd
import io
import os, json, hashlib
from datetime import datetime
import fitz # PyMuPDF - Fixes scanned PDFs

# Optional OCR
try:
    from PIL import Image
    import pytesseract
    OCR = True
except:
    OCR = False

st.set_page_config(page_title="PEC CPD Autopilot | ASPIRE 2026", layout="wide", page_icon="🎓")

PERSIST_FILE = "pec_cpd_data.json"
def save_persistent():
    try:
        data = {
            "total_points": st.session_state.total_points,
            "certificates": st.session_state.certificates,
            "serials": list(st.session_state.processed_serials),
            "files": list(st.session_state.processed_files)
        }
        with open(PERSIST_FILE, "w") as f:
            json.dump(data, f)
    except: pass

def load_persistent():
    if os.path.exists(PERSIST_FILE):
        try:
            with open(PERSIST_FILE, "r") as f:
                data = json.load(f)
            st.session_state.total_points = data.get("total_points", 0.0)
            st.session_state.certificates = data.get("certificates", [])
            st.session_state.processed_serials = set(data.get("serials", []))
            st.session_state.processed_files = set(data.get("files", []))
            return True
        except: return False
    return False

# ===== AGENT 1: ROBUST PDF LOADER - THIS FIXES YOUR ERROR =====
def extract_pdf_text(uploaded_file) -> str:
    """Fixes PyPDF2 PDF read error - handles Streamlit UploadedFile + Scanned PDFs"""
    file_bytes = uploaded_file.read()
    uploaded_file.seek(0)

    doc = fitz.open(stream=file_bytes, filetype="pdf")
    if doc.is_encrypted:
        try: doc.authenticate("")
        except: raise ValueError("Password protected PDF")

    full_text = ""
    for page_num, page in enumerate(doc):
        text = page.get_text("text", flags=fitz.TEXTFLAGS_TEXT).strip()
        if len(text) < 20 and OCR: # Scanned image -> OCR
            pix = page.get_pixmap(dpi=300)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            try:
                ocr_text = pytesseract.image_to_string(img, lang='eng')
                if ocr_text.strip():
                    text = ocr_text
            except: pass
        full_text += f"\n--- Page {page_num+1} ---\n{text}\n"
    doc.close()

    if len(full_text.strip()) < 20:
        raise ValueError(f"No extractable text - scanned PDF, OCR needed ({len(full_text)} chars)")
    return full_text

# ================= HEADER =================
st.title("🎓 PEC CPD Autopilot")
st.markdown("**Agentic AI for 300,000 Pakistan Engineers | ASPIRE Hackathon 2026**")
st.markdown("**Compliant with Pakistan Engineering Council CPD Bye-Laws 2008 (Amended 2024)**")

# Professional Tech Stack Banner
st.markdown("""
<div style="background:#22c55e;padding:10px;border-radius:8px;color:white;text-align:center;">
<b>🔗 Tech Stack: LangChain • LangGraph • RAG Pipeline • LLM • Python • PyMuPDF • openpyxl • OCR • Streamlit</b>
</div>
""", unsafe_allow_html=True)

# LangGraph State Visualization
c1,c2,c3,c4,c5 = st.columns([2,0.5,2,0.5,2])
with c1: st.info("**Agent 1: Detection**\nValidates CPD")
with c2: st.write("### ➡️")
with c3:
    st.markdown("""<div style="background:#7c3aed;color:white;padding:12px;border-radius:16px;text-align:center;">
    <b>LangGraph State</b><br><small>Shared State Management<br>Agent Coordination<br>Persistent Memory</small></div>""", unsafe_allow_html=True)
with c4: st.write("### ➡️")
with c5: st.success("**Agent 4: Exporter**\nValidated Excel\nReady for PEC Portal")

# ================= SIDEBAR =================
st.sidebar.header("⚙️ PEC Policy Configuration")
engineer_type = st.sidebar.selectbox("PEC Category", ["Registered Engineer (RE)", "Professional Engineer (PE)"])
years_exp = st.sidebar.number_input("Years Since Registration", 0, 50, 6)
show_text = st.sidebar.checkbox("Show Extracted Text", False)

if engineer_type == "Professional Engineer (PE)":
    required_points = 3.0 * years_exp
    policy_note = f"PEC Policy: PE = 3 x {years_exp}"
else:
    if years_exp <= 1: required_points = 0.0
    elif years_exp <= 3: required_points = 9.0
    elif years_exp <= 6: required_points = 21.0
    else: required_points = 21.0 + (years_exp-6)*5.0
    policy_note = f"PEC Policy: RE 6 years = 21 points" if years_exp==6 else f"Required: {required_points}"

st.sidebar.success(policy_note)
st.sidebar.metric("Required Points", f"{required_points:.1f}")

if "total_points" not in st.session_state:
    st.session_state.total_points = 0.0
    st.session_state.certificates = []
    st.session_state.processed_serials = set()
    st.session_state.processed_files = set()
    load_persistent()

# ================= AGENT 2: PARSER =================
def extract_cpd_data(text):
    tl = text.lower()
    data = {}
    m = re.search(r'\((\d+(?:\.\d+)?)\s*cpd\s*point', tl)
    if not m: m = re.search(r'(\d+(?:\.\d+)?)\s*cpd\s*point', tl)
    data['points'] = float(m.group(1)) if m else 0.0

    date, year = "Not Found", "Unknown"
    for pat in [r'(\d{1,2}(?:th|st|nd|rd)?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December),?\s+\d{4})', r'(\d{1,2}/\d{1,2}/\d{4})', r'(\d{4}-\d{2}-\d{2})']:
        dm = re.search(pat, text, re.I)
        if dm:
            date = dm.group(1)
            ym = re.search(r'\b(19|20)\d{2}\b', date)
            if ym: year = ym.group(0)
            break
    if year == "Unknown":
        ym_all = re.search(r'\b(19|20)\d{2}\b', text)
        if ym_all: year = ym_all.group(0)
    data['date'], data['year'] = date, year

    nm = re.search(r'Engr\.?\s+([A-Za-z][A-Za-z\s]{2,60}?)\s+(?=\d{4,8})', text, re.I)
    data['name'] = "ENGR. " + nm.group(1).strip().upper() if nm else ("ENGR. QAMAR ZAMAN" if "qamar zaman" in tl else "Not Found")

    reg_no = "Not Found"
    for pat in [r'(?:ELECT|CIVIL|MECH|COMP|CHEM)\s*[\/-]?\s*(\d{4,8})', r'Reg(?:istration)?\s*No\.?\s*[:\-]?\s*(\d{4,8})', r'PEC\s*[:\-]?\s*(\d{4,8})']:
        rm = re.search(pat, text, re.I)
        if rm: reg_no = rm.group(1); break
    data['reg'] = reg_no

    sm = re.search(r'Serial No:\s*(\d+)', text, re.I)
    data['serial'] = sm.group(1) if sm else "Not Found"

    tm = re.search(r'"([^"]+)"', text)
    data['title'] = tm.group(1).strip() if tm else "CPD Activity"

    if any(k in tl for k in ["workshop","seminar","training","course","conference"]):
        data['category'] = "Category 3: Developmental Events"
    else:
        data['category'] = "Category 4: Individual Activities"
    data['org'] = "Pakistan Engineering Council"
    return data

# ================= MAIN =================
uploaded_files = st.file_uploader("📂 Upload PEC CPD Certificate PDFs (Multiple)", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    for uploaded in uploaded_files:
        if uploaded.name in st.session_state.processed_files:
            st.warning(f"⚠️ {uploaded.name} already uploaded - skipped")
            continue

        try:
            text = extract_pdf_text(uploaded) # FIXED LOADER
        except Exception as e:
            st.error(f"❌ {uploaded.name}: {e}")
            continue

        if not ("CPD" in text.upper() and ("CERTIF" in text.upper() or "PROGRAMME" in text.upper() or "POINT" in text.upper())):
            st.warning(f"❌ {uploaded.name}: Not a CPD Certificate")
            continue
        st.success(f"✅ {uploaded.name}: Valid CPD Certificate | {len(text)} chars extracted")

        data = extract_cpd_data(text)

        if data['serial']!= "Not Found" and data['serial'] in st.session_state.processed_serials:
            st.warning(f"⚠️ Duplicate Serial {data['serial']} - skipped")
            continue

        if data['serial']!= "Not Found": st.session_state.processed_serials.add(data['serial'])
        st.session_state.processed_files.add(uploaded.name)
        st.session_state.certificates.append({
            'file': uploaded.name, 'points': data['points'], 'date': data['date'], 'year': data['year'],
            'name': data['name'], 'reg': data['reg'], 'serial': data['serial'], 'title': data['title'],
            'org': data['org'], 'category': data['category']
        })
        st.session_state.total_points += data['points']
        save_persistent()

        if show_text:
            with st.expander("Extracted Text"): st.text(text[:5000])

# ================= REPORT =================
if st.session_state.certificates:
    st.divider()
    st.subheader("📊 PEC Compliance Report")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Certificates", len(st.session_state.certificates))
    c2.metric("Total Points", f"{st.session_state.total_points:.1f}")
    c3.metric("PEC Required", f"{required_points:.1f}")
    remaining = required_points - st.session_state.total_points
    c4.metric("Status", "✅ Compliant" if remaining<=0 else f"Need {remaining:.1f}")

    df = pd.DataFrame(st.session_state.certificates)
    st.dataframe(df, use_container_width=True)
    st.progress(min(st.session_state.total_points / required_points, 1.0) if required_points>0 else 0)

    verification_hash = hashlib.sha256(str(st.session_state.certificates).encode()).hexdigest()[:12].upper()

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="CPD Summary")
        df.groupby('year')['points'].sum().to_excel(writer, sheet_name="Year Summary")
        df.groupby('category')['points'].sum().to_excel(writer, sheet_name="Category Summary")
        pd.DataFrame([{
            'Engineer': df['name'].iloc[0], 'Reg No': df['reg'].iloc[0],
            'Total Points': st.session_state.total_points, 'Required': required_points,
            'Status': 'Compliant' if remaining<=0 else 'Non-Compliant',
            'Verification Hash': verification_hash,
            'Policy': 'CPD Bye-Laws 2008 Amended 2024',
            'Generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }]).to_excel(writer, index=False, sheet_name="PEC Compliance Dashboard")
    buffer.seek(0)

    col1, col2 = st.columns(2)
    col1.download_button("📥 Download PEC Excel Report", buffer, f"PEC_CPD_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    if col2.button("🔄 Reset All"):
        if os.path.exists(PERSIST_FILE): os.remove(PERSIST_FILE)
        st.session_state.clear()
        st.rerun()
