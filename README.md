# PEC CPD Autopilot

**PEC CPD Autopilot - Agentic AI for 300,000 Pakistan Engineers**
**ASPIRE Final Hackathon 2026 | PEC CPD Points Calculator**
**Compliant with Pakistan Engineering Council CPD Bye-Laws 2008 (Amended 2024) | Verified from pec.org.pk**

## Live Demo & Repo

**Live Demo:** https://pec-cpd-autopilot-rfr4wbgq.streamlit.app/
**GitHub Repo:** https://github.com/qz59228/PEC-CPD-Autopilot
**Author:** Engr. Qamar Zaman | PEC Reg No: 137429

## Result - 2026 (Live App Data)

**Total CPD Points: 74.5 - PEC COMPLIANT**

- 2022: 6 Points
- 2023: 3 Points
- 2024: 2 Points
- 2025: 30 Points
- 2026: 31 Points
- Unknown: 2.5 Points
- **Certificates Processed: 76**
- **Calculation: 6 + 3 + 2 + 30 + 31 + 2.5 = 74.5**

**Engineer Type:** Registered Engineer (RE)
**Years Since Registration:** 6 Years
**PEC Required Points (RE 6 Years):** 21.0 Points
**Earned Points:** 74.5 Points
**Status:** ✅ Compliant - License Renewal Ready
**EPE Eligible:** ✅ Yes - 17 CPD Points + 5 Years Experience Completed (PEC CPD Bye-Laws 2008)
**Verification Hash:** 0199AA4476E7
**Report Generated:** 2026-10-04

![Architecture](architecture.jpg)

## Problem

Pakistan Engineering Council requires CPD Points for License Renewal. Engineers manually calculate from 76+ PEC PDFs - takes hours, prone to errors, duplicate counting, and missing year-wise distribution.

PEC Policy is complex:
- PE: 3 points per year
- RE First 3 Years: 9 points
- RE 6 Years: 21 points (9 + 12)
- RE After 6 Years: 5 points per year
- EPE: 17 CPD Points + 5 years experience required

## Solution

4-Agent LangGraph System auto-extracts, classifies, calculates, and exports PEC Excel in seconds. Duplicate detection by Serial No and File Name ensures no double counting. Persistent storage ensures data survives refresh.

## Features (Integrated in app.py)

- **Upload PEC CPD PDFs** - Multiple PDF upload, 76 certificates processed
- **Agent 1 - Ingestion Agent** - PyMuPDF / PyPDF2, extracts text from PEC PDF/Excel
- **Agent 2 - Classification Agent** - LLM Year Distribution: 2022:6, 2023:3, 2024:2, 2025:30, 2026:31, Sr# Extraction, Categorizes by year, Unlimited Year Extractor
- **Agent 3 - Calculator Agent** - BPA Logic, Grand Total 74.5 Validation, Duplicate Check, CA/192/2022 Rule, Validates totals and compliance
- **Agent 4 - Exporter Agent** - openpyxl, PEC Excel + BOQ Export, Generates validated outputs, 4-Sheet Report (CPD Summary, Year Summary, Category Summary, PEC Compliance Dashboard)
- **LangGraph State** - Shared State Management, Agent Coordination & Workflow Control, Persistent Memory & Context Passing
- **Duplicate Detection** - By Serial No (Primary) + File Name (Secondary), saved in pec_cpd_data.json, survives refresh
- **PEC Policy Sidebar** - RE/PE selector, Years Experience input, Required Points auto-calculated
- **EPE Eligibility Checker** - Checks 17 CPD Points + 5 Years Experience as per PEC CPD Bye-Laws 2008
- **PEC Official Compliance Seal** - Verification Hash (SHA256), Engineer Name, PEC Reg No: 137429, Total Points: 74.5, Required Points: 21.0, Compliance Status, EPE Status, Report Generated Timestamp, Engineer Signature field, PEC Authorized Officer Signature field
- **Persistent Storage** - pec_cpd_data.json, Data restored after refresh
- **Download Validated PEC Excel File** - Ready for Submission
- **Analytics** - Certificates by Year (Bar Chart), Points per Year, Points by PEC Category

## Architecture

![Architecture](architecture.jpg)

**Multi-Agent System:** Agent 1 Detection | Agent 2 Parser | Agent 3 Validator (Duplicate Check) | Agent 4 Exporter

## Tech Stack

LangChain, LangGraph, LLM, RAG Pipeline, Python, PyMuPDF, PyPDF2, openpyxl, pandas, Streamlit, hashlib

## How to Run

1. Clone repo
2. pip install -r requirements.txt
3. streamlit run app.py
4. Upload PDFs -> Get Total -> Download Excel

## PEC Policy Reference

- PEC CPD Bye-Laws 2008 (Amended 2024) - pec.org.pk
- Professional Engineer (PE): 3 points per year x Years Experience
- Registered Engineer (RE): 9 points first 3 years, 21 points for 6 years, 5 points per year after 6 years
- EPE Eligibility: 17 CPD Points + 5 years experience
- PEC Categories: Category 1 Formal Education, Category 2 Work Based, Category 3 Developmental Events, Category 4 Individual Activities

## Hackathon 2026

**ASPIRE Final Hackathon 2026**

- **Innovation:** 4-Agent AI system extracts real PEC PDFs automatically
- **Technical:** LangGraph-like state, persistent storage, unlimited year extractor, duplicate validator, professional regex
- **Impact:** 300,000 Pakistan Engineers, PEC license renewal, EPE eligibility checker
- **Authentic:** 100% real PEC certificates 2022-2026, PEC policy compliant, no demo data, 76 certificates verified
- **Professional:** Production ready, survives refresh, 4-sheet PEC Excel report

## Legal Disclaimer

This is an engineer-generated summary extracted from uploaded PEC certificates. It is not an official PEC issued document and does not claim PEC endorsement. All data is extracted directly from real PEC certificates uploaded by the engineer. For official PEC verification, certificates must be verified with Pakistan Engineering Council directly at pec.org.pk. This application is developed for ASPIRE Final Hackathon 2026 for educational and automation purposes only.
