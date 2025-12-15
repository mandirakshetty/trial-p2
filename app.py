import streamlit as st
import os
from datetime import datetime

ROOT = r"E:/LogSpace"

# ------------------------------------------------------------
# Helper: find logs based on input
# ------------------------------------------------------------
def find_logs(client, logspace, version):
    """Navigate the folder structure and return matched error/info logs."""

    results = {"error_logs": [], "info_logs": []}

    # Search recursive for matching folders
    for root, dirs, files in os.walk(ROOT):
        if client.lower() in root.lower() and logspace.lower() in root.lower() and version in root:
            for f in files:
                fpath = os.path.join(root, f)
                if f.endswith(".error"):
                    with open(fpath, "r", encoding="utf-8") as ef:
                        results["error_logs"].append(ef.read())
                elif f.endswith(".info"):
                    with open(fpath, "r", encoding="utf-8") as inf:
                        results["info_logs"].append(inf.read())
    return results

# ------------------------------------------------------------
# Placeholder RCA generator (later replaced with AWS Bedrock)
# ------------------------------------------------------------
def generate_rca(logs, timestamp, version):
    """Produce justifiable RCA text from logs."""

    error_count = sum(len(l.splitlines()) for l in logs["error_logs"])
    info_count = sum(len(l.splitlines()) for l in logs["info_logs"])

    if error_count == 0:
        return (
            "No critical issues were detected in the provided logs.\n"
            "The system appears to be in a stable state with no major failure patterns."
        )

    # Simple heuristic for trial prototype
    return f"""
Root Cause Analysis Summary
---------------------------

Timestamp Evaluated: {timestamp}
System Version: {version}

A total of {error_count} error log entries were detected.  
These errors indicate recurring failure patterns in one or more components.

Based on the analyzed logs, the system likely experienced:

1. **Component or service instability**, shown by repeated ERROR events.
2. Possible **network, API, or configuration-related issues**, based on error patterns.
3. Multiple INFO logs indicate that certain system modules were still operational.

This suggests a **partial service degradation**, not a complete outage.

Recommended Actions:
- Validate configuration settings for the affected service.
- Verify network/API connectivity.
- Restart or redeploy unstable components.

(This is the prototype logic. You will replace this with Bedrock + RAG reasoning.)
"""

# ------------------------------------------------------------
# Streamlit UI
# ------------------------------------------------------------
st.set_page_config(page_title="AI Log Analyzer", layout="wide")

st.title("Enterprise LogSpace Analyzer Prototype")
st.write("Phase-2 UI • Splunk-like log inspection dashboard")

st.markdown("---")

# --------------------------- Input Panel --------------------
with st.sidebar:
    st.header("Input Parameters")

    client = st.text_input("Client Name (ex: Barclays / SBI / BankOfAmerica)")
    logspace = st.text_input("LogSpace Name (ex: Unigy / Pulse / Touch)")
    timestamp = st.text_input("Timestamp", value=str(datetime.utcnow()))
    version = st.text_input("System Version (ex: 4.0.1)")

    submitted = st.button("Analyze Logs")

# --------------------------- Output Section ------------------
if submitted:
    if not (client and logspace and timestamp and version):
        st.error("Please fill all fields.")
    else:
        st.subheader("1. Searching LogSpace Folders...")
        logs = find_logs(client, logspace, version)

        st.write(f"Found {len(logs['error_logs'])} error log file(s).")
        st.write(f"Found {len(logs['info_logs'])} info log file(s).")

        st.markdown("---")
        st.subheader("2. Log Preview")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Error Logs")
            if logs["error_logs"]:
                for l in logs["error_logs"]:
                    st.code(l, language="text", wrap_lines=True)
            else:
                st.info("No error logs found.")

        with col2:
            st.markdown("### Info Logs")
            if logs["info_logs"]:
                for l in logs["info_logs"]:
                    st.code(l, language="text", wrap_lines=True)
            else:
                st.info("No info logs found.")

        st.markdown("---")
        st.subheader("3. RCA Output (Prototype)")

        rca = generate_rca(logs, timestamp, version)
        st.write(rca)
