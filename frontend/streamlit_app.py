import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

# ── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ── Session State Init ──────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "password" not in st.session_state:
    st.session_state.password = ""
if "role" not in st.session_state:
    st.session_state.role = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []   # stores {role, content} dicts


# ── Login Page ──────────────────────────────────────────────────────────────
def show_login():
    st.title("🔐 Login")
    st.caption("Enter your credentials to access the RAG system")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        if not username or not password:
            st.error("Please enter both username and password")
            return

        try:
            response = requests.get(
                f"{BASE_URL}/login",
                auth=(username, password)   # Basic Auth
            )

            if response.status_code == 200:
                data = response.json()
                # Save to session state
                st.session_state.logged_in = True
                st.session_state.username  = username
                st.session_state.password  = password
                st.session_state.role      = data["role"]
                st.rerun()                  # go to chat page

            elif response.status_code == 401:
                st.error("❌ Invalid username or password")

            else:
                st.error(f"Something went wrong: {response.status_code}")

        except requests.exceptions.ConnectionError:
            st.error("⚠️ Cannot connect to backend. Is FastAPI running?")


# ── Chat Page ───────────────────────────────────────────────────────────────
def show_chat():
    # Header
    st.title("🤖 RAG Chatbot")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.caption(f"Logged in as **{st.session_state.username}** | Role: `{st.session_state.role}`")
    with col2:
        if st.button("Logout", use_container_width=True):
            # Clear session and go back to login
            st.session_state.logged_in   = False
            st.session_state.username    = ""
            st.session_state.password    = ""
            st.session_state.role        = ""
            st.session_state.chat_history = []
            st.rerun()

    st.divider()

    # ── Scrollable Chat History ─────────────────────────────────────────────
    chat_container = st.container(height=500)    # scrollable when long
    with chat_container:
        if not st.session_state.chat_history:
            st.info("Ask me anything! I'll answer based on your access level.")
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):   # "user" or "assistant"
                st.write(msg["content"])

    # ── Input Box + Send ────────────────────────────────────────────────────
    user_input = st.chat_input("Type your question here...")

    if user_input:
        # Add user message to history immediately
        st.session_state.chat_history.append({
            "role":    "user",
            "content": user_input
        })

        # Send to /chat endpoint
        try:
            response = requests.post(
                f"{BASE_URL}/chat",
                auth=(st.session_state.username, st.session_state.password),
                json={"message": user_input}     # ChatRequest shape
            )

            if response.status_code == 200:
                data = response.json()
                # Add assistant reply to history
                st.session_state.chat_history.append({
                    "role":    "assistant",
                    "content": data["answer"]    # ChatResponse.answer
                })

            elif response.status_code == 401:
                st.error("Session expired. Please login again.")
                st.session_state.logged_in = False
                st.rerun()

            else:
                st.error(f"Error from backend: {response.status_code}")

        except requests.exceptions.ConnectionError:
            st.error("⚠️ Cannot connect to backend. Is FastAPI running?")

        st.rerun()   # refresh to show new messages


# ── Router ──────────────────────────────────────────────────────────────────
if st.session_state.logged_in:
    show_chat()
else:
    show_login()