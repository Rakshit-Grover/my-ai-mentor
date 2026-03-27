import streamlit as st
import google.generativeai as genai
import datetime

# App UI Configuration
st.set_page_config(page_title="Gemclaude GPT Terminal", page_icon="🛰️")
st.title("Gemclaude GPT // Mentor Terminal")
st.markdown("<span style='color: #0ea5e9; font-weight: bold; border: 1px solid #0ea5e9; padding: 2px 8px; border-radius: 5px;'>● MENTOR PROTOCOL ACTIVE</span>", unsafe_allow_html=True)
st.markdown("---")

# Secure API Key Input
api_key = st.sidebar.text_input("Enter Google API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # The Master Directives (All Features Combined)
        system_instruction = """
        You are Gemclaude GPT, an elite AI mentor for Rakshit, an 8th-grade ICSE student in Jalandhar, Punjab, who wants to be an astronaut. 
        
        Your Rules:
        1. Personality & Thinking: You think deeply and logically. You maintain a strict, disciplined 'Mentor' persona, but you are always helpful. Zero useless talk.
        2. Unblocked Assistance: Answer his questions directly, write code, or help him with his mechanical design projects. NEVER block his requests with a test first.
        3. Image Generation Capability: If he asks you to generate an image, you MUST output it using this exact Markdown format: ![Image](https://image.pollinations.ai/prompt/detailed-description-of-the-image-with-words-separated-by-hyphens). 
           Example: ![Image](https://image.pollinations.ai/prompt/a-highly-detailed-space-station-orbiting-mars-cinematic-lighting).
        4. The 72-Hour Rule: If the system secretly tells you that 72 hours have passed, you must add ONE Class 8 ICSE syllabus question (Math, Physics, or Computer) at the very bottom of your response.
        5. 360-Degree Perspective: Occasionally ask him to explain his exact reasoning to make him think like an engineer.
        """
        
        # Using the fast Flash model to avoid quota errors
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction
        )

        # Initialize Memory and the Python Clock
        if "chat_session" not in st.session_state:
            st.session_state.chat_session = model.start_chat(history=[])
        
        # Set the timer so it asks a question on the very first chat, then waits exactly 3 days
        if "last_test_time" not in st.session_state:
            st.session_state.last_test_time = datetime.datetime.now() - datetime.timedelta(hours=72)

        # Render Previous Transmissions
        for message in st.session_state.chat_session.history:
            role = "Rakshit" if message.role == "user" else "Gemclaude GPT"
            with st.chat_message("user" if role == "Rakshit" else "assistant"):
                # Hide the secret timer code from the UI
                display_text = message.parts[0].text.split("\n\n[System Timer:")[0]
                st.markdown(display_text.strip())

        # Command Input
        user_input = st.chat_input("Awaiting your command, Cadet...")
        
        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)
                
            # The 72-Hour Logic Gate
            current_time = datetime.datetime.now()
            time_passed = current_time - st.session_state.last_test_time
            
            if time_passed.total_seconds() >= (72 * 3600):
                # 72 hours have passed! Secretly tell the AI to add a question.
                final_prompt = user_input + "\n\n[System Timer: 72 hours have passed. Add an ICSE Class 8 question at the end of your response.]"
                st.session_state.last_test_time = current_time # Reset the stopwatch
            else:
                final_prompt = user_input
            
            with st.chat_message("assistant"):
                response = st.session_state.chat_session.send_message(final_prompt)
                
                # Hide the timer from the AI's current response just in case it repeats it
                clean_response = response.text.replace("[System Timer: 72 hours have passed. Add an ICSE Class 8 question at the end of your response.]", "")
                st.markdown(clean_response.strip())
                
    except Exception as e:
        st.error(f"System Error Detected: {e}")
        
else:
    st.info("👈 SYSTEM LOCKED. Enter your API key in the sidebar.")
