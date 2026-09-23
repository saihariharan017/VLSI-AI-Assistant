import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

st.set_page_config(page_title="AI Research Agent", layout="wide")

st.title("AI Research Agent")
st.write("Enter topics to generate research reports")

topics_input = st.text_area(
    "Enter topics (one per line)",
    height=150
)

if st.button("Generate Report"):

    if topics_input.strip() == "":
        st.warning("Please enter at least one topic")
    else:
        topics = topics_input.split("\n")

        for topic in topics:
            topic = topic.strip()
            if topic:
                st.subheader(f"Researching: {topic}")

                result = run_research(topic)

                st.success("Report generated")
                st.write(result)
