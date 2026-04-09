import streamlit as st
from main import run_war_room

st.set_page_config(page_title="AI Launch War Room", layout="centered")

st.title("🚀 AI Product Launch War Room")

st.write(
    "This system simulates a cross‑functional war room "
    "using multiple AI agents to decide whether to proceed, pause, or roll back a launch."
)

if st.button("Run War Room Simulation"):
    with st.spinner("Agents are analyzing the launch..."):
        result = run_war_room()

    st.subheader("📌 Final Decision")
    st.success(result["decision"])

    st.subheader("🧠 Rationale")
    st.json(result)