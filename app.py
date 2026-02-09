from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# --- Configuration (SECURE - No hardcoded key!) ---
load_dotenv()
if 'GEMINI_API_KEY' in st.secrets:
    genai.configure(api_key=st.secrets['GEMINI_API_KEY'])
else:
    st.error("❌ Add GEMINI_API_KEY to .streamlit/secrets.toml")
    st.stop()

# --- Utility Functions ---
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        return [{"mime_type": uploaded_file.type, "data": bytes_data}]
    return None

def get_gemini_response(input_text, image_data, prompt):
    full_prompt = f"{prompt}\n\nUser Instruction: {input_text}"
    
    # ✅ THESE MODELS WORK IN FEBRUARY 2026:
    model = genai.GenerativeModel("gemini-2.5-flash")  # ✅ STABLE & FAST
    
    if image_data:
        response = model.generate_content([full_prompt, image_data[0]])
    else:
        response = model.generate_content(full_prompt)
    
    return response.text

# --- Streamlit Page Settings ---
st.set_page_config(page_title="🏺 Gemini Artifact Insight AI", page_icon="🏺", layout="centered")

# --- Custom CSS (Your styling - PERFECT) ---
st.markdown("""
    <style>
        .stApp {background-color: #ecf0f3; font-family: 'Verdana', sans-serif; color: #222222;}
        .title {font-family: 'Georgia', serif; font-size: 36px; font-weight: 700; color: black; text-align: center;}
        .stButton button {background-color: #4B47C3; color: white; border-radius: 8px;}
        .stButton button:hover {background-color: #3934a1;}
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="title">🏺 Gemini Artifact Insight AI</div>', unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.header("📥 Upload Inputs")
    uploaded_file = st.file_uploader("Upload Artifact Image", type=["jpg", "jpeg", "png"])
    input_text = st.text_area("📌 Add Context (optional)", 
                             placeholder="What do you want to know about this artifact?")
    submit = st.button("🔍 Generate Description", type="primary")

# --- Show Image ---
if uploaded_file:
    st.image(uploaded_file, caption="🖼 Uploaded Artifact", use_container_width=True)

# --- System Prompt ---
system_prompt = """
You are an expert historian. Analyze the artifact image and provide:
- Name/identification
- Historical period/origin  
- Materials used
- Cultural significance
- Interesting facts
Keep response detailed but engaging (300-500 words).
"""

# --- Generate Response ---
if submit:
    if not uploaded_file:
        st.warning("⚠️ Please upload an artifact image first!")
    else:
        try:
            with st.spinner("🔍 AI is analyzing your artifact..."):
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response(input_text or "Describe this artifact", image_data, system_prompt)

            st.success("✅ Analysis complete!")
            st.markdown("### 📜 Artifact Analysis")
            st.markdown(response)

            # Download
            st.download_button("📥 Download Report", response, "artifact_report.txt", "text/plain")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("🔧 Fix: Check API quota, try smaller image, or regenerate API key")

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #666;'>Powered by Gemini 2.5 Flash • For SmartInternz Project</p>", unsafe_allow_html=True)
