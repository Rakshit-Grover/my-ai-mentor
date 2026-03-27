import streamlit as st
import google.generativeai as genai

# App UI Configuration
st.set_page_config(page_title="Rakshit's AI Mentor", page_icon="🚀")
st.title("My Personal AI Mentor")
st.markdown("---")

# Secure API Key Input via Sidebar
api_key = st.sidebar.text_input("Enter Google API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # The Updated, Normal Mentor Directives
        system_instruction = """
        You are a helpful, knowledgeable, and friendly AI mentor for Rakshit, an 8th-grade ICSE student in Jalandhar, Punjab. His ultimate goal is to become an astronaut, and he is passionate about coding and AI.
        
        Your Rules:
        1. Be a friendly, supportive, and clear mentor. Speak normally and straightforwardly.
        2. Help him with his coding, AI research, and schoolwork by breaking complex topics down into easy-to-understand language.
        3. Occasional Testing: Every so often (but not every single time he talks to you), naturally weave in a question related to the Class 8 ICSE syllabus (Math, Science, or Computer) to test his knowledge and keep him sharp.
        4. If he makes a mistake, politely correct him and explain the right way to think about it.
        5. Generate Class 8 ICSE practice papers whenever he asks for them.
        """
        
        model = genai.GenerativeModel(
            model_name="gemini-pro",
            system_instruction=system_instruction
        )

        # Initialize Memory
        if "chat_session" not in st.session_state:
            st.session_state.chat_session = model.start_chat(history=[])

        # Render Previous Transmissions
        for message in st.session_state.chat_session.history:
            role = "Rakshit" if message.role == "user" else "AI Mentor"
            with st.chat_message("user" if role == "Rakshit" else "assistant"):
                st.markdown(message.parts[0].text)

        # Command Input
        user_input = st.chat_input("Ask me anything...")
        
        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)
                
            with st.chat_message("assistant"):
                response = st.session_state.chat_session.send_message(user_input)
                st.markdown(response.text)
                
    except Exception as e:
        st.error(f"System Error Detected: {e}")
        
else:
    st.info("👈 Please enter your API key in the sidebar to start chatting.")
