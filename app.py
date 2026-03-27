import streamlit as st
import google.generativeai as genai

# App UI Configuration (Clean, Gemini-like UI)
st.set_page_config(page_title="Gemclaude GPT Terminal", page_icon="🛰️")
st.title("Gemclaude GPT // Mentor Terminal")
st.markdown("<span style='color: #ef4444; font-weight: bold; border: 1px solid #ef4444; padding: 2px 8px; border-radius: 5px;'>● STRICT PROTOCOL ACTIVE</span>", unsafe_allow_html=True)
st.markdown("---")

# Secure API Key Input via Sidebar
api_key = st.sidebar.text_input("Enter Google API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # The Master Directives (Personality, Intelligence, and Image Generation)
        system_instruction = """
        You are Gemclaude GPT, an elite, highly intelligent, and incredibly strict AI mentor.
        Your student is Rakshit, an 8th-grade ICSE student in Jalandhar, Punjab, who wants to be an astronaut. He is a Krishna bhakt, valuing immense focus, duty, and discipline.
        
        Your Rules:
        1. Strict & Fatherly: Be straightforward, harsh, and demand perfection. Zero useless talk.
        2. Brutally Honest: If he makes a mistake, scold him immediately. Remind him that in space travel and advanced coding, a single miscalculation is catastrophic.
        3. The 'Lock' Protocol: Whenever he asks you to generate something (code, research, answers, or images), FIRST give him a difficult test based on the Class 8 ICSE math, physics, or computer syllabus. Do not fulfill his request until he provides the correct logical answer.
        4. Image Generation Capability: If he passes your test and asks you to generate an image, you MUST output an image using this exact Markdown format: ![Image](https://image.pollinations.ai/prompt/detailed-description-of-the-image-with-words-separated-by-hyphens). 
           Example: ![Image](https://image.pollinations.ai/prompt/a-highly-detailed-space-station-orbiting-mars-cinematic-lighting). This will automatically render a generated image in his user interface.
        5. 360-Degree Perspective: Ask him to explain his exact reasoning for his answers. Force him to look at problems from an engineer's perspective.
        """
        
        # Using the advanced Pro model found in your diagnostic
        model = genai.GenerativeModel(
            model_name="gemini-2.5-pro",
            system_instruction=system_instruction
        )

        # Initialize Memory
        if "chat_session" not in st.session_state:
            st.session_state.chat_session = model.start_chat(history=[])

        # Render Previous Transmissions
        for message in st.session_state.chat_session.history:
            role = "Rakshit" if message.role == "user" else "Gemclaude GPT"
            with st.chat_message("user" if role == "Rakshit" else "assistant"):
                st.markdown(message.parts[0].text)

        # Command Input
        user_input = st.chat_input("Awaiting your command, Cadet...")
        
        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)
                
            with st.chat_message("assistant"):
                response = st.session_state.chat_session.send_message(user_input)
                st.markdown(response.text)
                
    except Exception as e:
        st.error(f"System Error Detected: {e}")
        
else:
    st.warning("⚠️ SYSTEM LOCKED. Enter your API key in the sidebar to initiate the mentor protocol.")
