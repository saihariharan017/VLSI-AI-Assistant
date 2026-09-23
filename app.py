import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="VLSI AI Assistant",
    page_icon="🔬",
    layout="centered"
)

st.title("🔬 VLSI AI Assistant")
st.caption("Your AI assistant for VLSI Design, CMOS, Verilog, RTL, Physical Design and more.")

if not API_KEY:
    st.error("Gemini API key not found. Please check your Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = """
You are a specialized VLSI Engineering AI Assistant.

Your main purpose is to help students, engineers and researchers
understand VLSI and semiconductor design concepts.

You should answer questions related to:

1. VLSI fundamentals
2. Digital electronics
3. CMOS technology
4. MOSFET
5. Logic gates
6. Verilog HDL
7. SystemVerilog
8. RTL design
9. Logic synthesis
10. Static Timing Analysis
11. Clock design
12. Low-power VLSI
13. Power, Performance and Area
14. Physical Design
15. Floorplanning
16. Placement
17. Clock Tree Synthesis
18. Routing
19. Design for Testability
20. Semiconductor fabrication
21. ASIC design
22. FPGA
23. VLSI interview questions
24. VLSI viva questions
25. Verilog coding and debugging

Rules:

Give technically accurate answers.
Explain difficult concepts in simple language.
Use examples whenever useful.
For Verilog questions, provide clean and correct code.
Explain code line by line when requested.
For comparison questions, use tables when useful.
If the question is not related to VLSI, politely say that
you are primarily designed for VLSI-related questions.
Do not invent technical facts.
For beginners, explain concepts step-by-step.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask your VLSI question...")

if user_input:

    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    conversation = SYSTEM_PROMPT + "\n\n"

    for message in st.session_state.messages:
        conversation += (
            message["role"].upper()
            + ": "
            + message["content"]
            + "\n"
        )

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=conversation
                )

                answer = response.text
                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"Error: {e}")
