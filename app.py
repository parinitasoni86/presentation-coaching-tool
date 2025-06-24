# app.py  –  AI Elevator Pitch Generator (Streamlit + OpenAI v1+)

import os
import streamlit as st
from openai import OpenAI   # works with openai >= 1.0

# ---------------------------------------------------------------------
# 1. Configure your OpenAI API key
# ---------------------------------------------------------------------
# Preferred (secure) – set this in PowerShell **before** running the app:
#   $env:OPENAI_API_KEY = "sk-XXXXXXXXXXXXXXXXXXXXXXXX"
#
# If you need a quick test and understand the risk, you can hard-code it:
# os.environ["OPENAI_API_KEY"] = "sk-XXXXXXXXXXXXXXXXXXXXXXXX"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if client.api_key is None:
    st.error("🛑 OPENAI_API_KEY environment variable not found.")
    st.stop()

# ---------------------------------------------------------------------
# 2. Streamlit UI
# ---------------------------------------------------------------------
st.title("🗣️ AI Elevator Pitch Generator")

st.subheader("Enter Key Details for Your Pitch")
key_points = st.text_area(
    "Key points (comma-separated)",
    placeholder="e.g., AI coaching, real-time transcription, filler-word detection",
)
duration = st.selectbox("Choose pitch length", ["2 minutes", "3 minutes", "4 minutes"])

# ---------------------------------------------------------------------
# 3. Generate pitch on button click
# ---------------------------------------------------------------------
if st.button("Generate Elevator Pitch"):
    if not key_points.strip():
        st.warning("Please enter some key points.")
    else:
        with st.spinner("Generating your pitch…"):
            prompt = (
                f"Write a {duration} elevator pitch using the following points: "
                f"{key_points}. Make it concise, engaging, and relevant to sales enablement."
            )

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",            # use another model you have access to if needed
                messages=[{"role": "user", "content": prompt}],
            )

            pitch = response.choices[0].message.content.strip()
            st.success("Here’s your pitch!")
            st.write(pitch)