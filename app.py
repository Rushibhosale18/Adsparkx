import streamlit as st
import json
from dotenv import load_dotenv
from agent import SupportAgent

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Adsparkx AI - Support Agent", page_icon="✨", layout="centered")

# Custom CSS for a premium look
st.markdown("""
<style>
    /* Main background with subtle animated gradient */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        background-size: 200% 200%;
        animation: gradient 15s ease infinite;
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Headers with glowing text */
    h1 {
        background: -webkit-linear-gradient(45deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        padding-bottom: 20px;
        text-shadow: 0px 0px 20px rgba(56, 189, 248, 0.3);
    }
    
    /* Chat bubbles - Premium Glassmorphism */
    .stChatMessage {
        background-color: rgba(30, 41, 59, 0.4);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        transition: transform 0.2s ease-in-out;
    }
    
    .stChatMessage:hover {
        transform: translateY(-2px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: rgba(56, 189, 248, 0.05);
        border-radius: 8px;
        color: #e0e7ff;
        border: 1px solid rgba(129, 140, 248, 0.2);
    }
    
    /* Input Container Glowing Effect */
    .stChatInputContainer {
        border-radius: 20px;
        border: 1px solid rgba(129, 140, 248, 0.3);
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.15);
        background-color: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(10px);
    }
    
    .stChatInputContainer:focus-within {
        border: 1px solid rgba(56, 189, 248, 0.8);
        box-shadow: 0 0 30px rgba(56, 189, 248, 0.4);
    }
</style>
""", unsafe_allow_html=True)

st.title("Adsparkx AI ✨")
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.1em; margin-bottom: 30px;'>Persona-Adaptive Customer Support Agent</p>", unsafe_allow_html=True)

# Initialize agent
@st.cache_resource
def get_agent():
    return SupportAgent()

try:
    agent = get_agent()
except Exception as e:
    st.error(f"Failed to initialize agent: {e}")
    st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display metadata for assistant messages
        if message["role"] == "assistant":
            with st.expander("Show Agent Details"):
                st.write(f"**Detected Persona:** {message.get('persona')}")
                st.write(f"**Retrieved Sources:** {', '.join(message.get('sources', []))}")
                st.write(f"**Escalated:** {message.get('escalated')}")
                if message.get("escalation_reason"):
                    st.write(f"**Escalation Reason:** {message.get('escalation_reason')}")
                if message.get("handoff_summary"):
                    st.json(message.get("handoff_summary"))

# Accept user input
if prompt := st.chat_input("How can I help you today?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing and retrieving information..."):
            try:
                result = agent.process_query(prompt)
                
                response = result["response"]
                persona = result["persona"]
                sources = result["sources"]
                escalated = result["escalated"]
                
                st.markdown(response)
                
                with st.expander("Agent Details (Persona, RAG, Escalation)", expanded=True):
                    st.write(f"**Detected Persona:** {persona}")
                    if sources:
                        st.write(f"**Retrieved Sources:** {', '.join(sources)}")
                    else:
                        st.write("**Retrieved Sources:** None")
                        
                    if escalated:
                        st.warning(f"**ESCALATED TO HUMAN**")
                        st.write(f"**Reason:** {result['escalation_reason']}")
                        st.subheader("Handoff Summary")
                        st.json(result["handoff_summary"])
                        
                # Add assistant message to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "persona": persona,
                    "sources": sources,
                    "escalated": escalated,
                    "escalation_reason": result.get("escalation_reason"),
                    "handoff_summary": result.get("handoff_summary")
                })
            except Exception as e:
                st.error(f"Error processing query: {e}")
