import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Initialize the generative AI model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
chat = model.start_chat(history=[])

def get_response(user_input):
    response = chat.send_message(user_input, stream=True)
    return response

def analyze_file(file):
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
            st.markdown("### File Preview")
            st.dataframe(df.head(), use_container_width=True)
            st.markdown("### Summary Statistics")
            st.dataframe(df.describe(), use_container_width=True)
        elif file.name.endswith('.txt'):
            content = file.read().decode('utf-8')
            st.markdown("### File Content")
            st.text_area("Content", content, height=300)
        else:
            st.error("Unsupported file format. Please upload a .csv or .txt file.")
    except Exception as e:
        st.error(f"Error analyzing file: {e}")

# Streamlit app layout
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")
st.title(" AI-Powered Chatbot")
st.markdown("<style>.main {text-align: center;}</style>", unsafe_allow_html=True)

# Sidebar for user input and history
with st.sidebar:
    st.header("🗂 Chat History")
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    if st.session_state['chat_history']:
        for entry in st.session_state['chat_history']:
            role = entry['role']
            message = entry['message']
            st.markdown(f"**{role}:** {message}")

# Main content for the chatbot
st.markdown("---")
st.subheader("💬 Let's Chat!")
col1, col2 = st.columns([3, 1])

with col1:
    user_input = st.text_input("Type your message here:", placeholder="Say something...")
with col2:
    submit = st.button("Send", use_container_width=True)

# File upload and analysis
st.markdown("---")
st.subheader("📂 Upload and Analyze Files")
file = st.file_uploader("Upload a CSV or TXT file for analysis", type=["csv", "txt"], label_visibility="collapsed")
if file:
    analyze_file(file)

# Process user input and generate response
if user_input and submit:
    response = get_response(user_input=user_input)
    st.session_state['chat_history'].append({"role": "You", "message": user_input})

    # Display the AI response incrementally
    st.markdown("### 🤖 AI's Response")
    for part in response:
        st.write(part.text)
        st.session_state['chat_history'].append({"role": "AI", "message": part.text})

# Footer
st.markdown("---")
st.caption("Powered by Gemini AI")
