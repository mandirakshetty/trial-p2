# src/ui_streamlit.py
import streamlit as st
import requests
import json
from datetime import datetime

API_URL = "http://localhost:8000/analyze"

st.set_page_config(page_title="RCA Enterprise Analyzer", layout="wide")
st.title("RCA Enterprise Analyzer (Phase 2)")

with st.form("analyze_form"):
    client = st.text_input("Client (e.g., Barclays, SBI, BankOfAmerica)")
    logspace = st.text_input("Application (e.g., Unigy, Pulse, Touch)")
    version = st.text_input("Version (e.g., 4.0.1)")
    timestamp = st.text_input("Timestamp (optional)", value=str(datetime.utcnow()))
    top_k = st.selectbox("Top K results", [1,2,3,5], index=2)
    uploaded = st.text_area("Optional: paste log text to analyze (overrides folder search)", height=120)
    submitted = st.form_submit_button("Analyze")

if submitted:
    payload = {
        "client": client,
        "logspace": logspace,
        "version": version,
        "timestamp": timestamp,
        "top_k": top_k,
    }
    if uploaded.strip():
        payload["uploaded_log_text"] = uploaded

    with st.spinner("Sending request to backend..."):
        r = requests.post(API_URL, json=payload, timeout=120)
    if r.status_code != 200:
        st.error(f"API Error: {r.status_code} {r.text}")
    else:
        data = r.json()
        st.subheader("RCA Results")
        for res in data["results"]:
            st.markdown("### Answer")
            st.code(res["answer"])
            st.markdown("#### Evidence")
            for e in res["evidence"]:
                st.write(f"score: {e['score']:.3f}")
                st.code(e['text'][:1000])
