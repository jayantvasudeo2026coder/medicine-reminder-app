import streamlit as st
from PIL import Image
from google import genai
from gtts import gTTS
import os

# Page Config
st.set_page_config(page_title="AI Prescription Reader", page_icon="💊", layout="centered")

st.title("💊 AI Prescription Reader & Medicine Reminder")
st.write("Upload a doctor's prescription image to parse medicine details and get reminders.")

# Sidebar for API Key
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

uploaded_file = st.file_uploader("Choose a prescription image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Prescription", use_container_width=True)

    if st.button("Analyze Prescription 🚀"):
        if not api_key:
            st.error("Kripya Sidebar mein Gemini API Key daalein!")
        else:
            with st.spinner("Analyzing image using AI Vision..."):
                try:
                    # Client initialize karein
                    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

                    prompt = """
                    You are an expert medical AI assistant. Analyze this prescription image and extract details in Hindi-English (Hinglish) with clear formatting:
                    1. **Medicine Name** (Dawaai ka naam)
                    2. **Dosage & Frequency** (Kitni baar aur kab leni hai)
                    3. **Duration** (Kitne din tak leni hai)
                    4. **Important Precautions** (Khas hidayat - e.g., khane ke baad ya pehle)
                    
                    Format the output nicely using bullet points and Markdown tables if necessary.
                    Add a strict disclaimer at the end: "Disclaimer: Always consult a certified pharmacist or doctor before taking medicines."
                    """

                    # Call Gemini 3.6 Flash Model
                    response = client.models.generate_content(
                        model='gemini-3.6-flash',
                        contents=[image, prompt]
                    )

                    result_text = response.text
                    
                    # Display Results
                    st.success("Analysis Complete!")
                    st.markdown("### 📋 Medicine Summary")
                    st.markdown(result_text)

                    # Text-to-Speech (Voice Assistance)
                    st.markdown("### 🔊 Audio Assistant")
                    tts = gTTS(text="Dawaai ki jankari taiyar hai. Kripya screen par diye gaye nirdesh dhyan se padhein.", lang='hi')
                    tts.save("voice.mp3")
                    st.audio("voice.mp3", format="audio/mp3")

                except Exception as e:
                    st.error(f"Error analyzing image: {e}")

# Static Demo for Medicine Reminder Feature
st.markdown("---")
st.markdown("### ⏰ Set Daily Medicine Reminder")
col1, col2 = st.columns(2)
with col1:
    med_name = st.text_input("Medicine Name", "Paracetamol 500mg")
with col2:
    med_time = st.time_input("Reminder Time")

if st.button("Set Reminder 🔔"):
    st.info(f"Reminder set for **{med_name}** at **{med_time}** successfully!")
    