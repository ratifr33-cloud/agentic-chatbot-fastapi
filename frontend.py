import streamlit as st
import requests

st.set_page_config(page_title="Agentic Chat", layout="centered")
st.title("Agentic Chat")
st.write("Ask a question and get an AI response.")

if "history" not in st.session_state:
    st.session_state.history = []
if "search_key" not in st.session_state:
    st.session_state.search_key = ""

with st.sidebar:
    st.title("History")
    if st.button("+ New chat"):
        st.session_state.history = []
        st.session_state.search_key = ""
    st.text_input("Search chat", key="search_key", placeholder="Filter messages")

    items = [m for m in st.session_state.history if st.session_state.search_key.lower() in m["text"].lower()]
    if items:
        for msg in items:
            prefix = "You" if msg["role"] == "user" else "Agent"
            st.markdown(f"**{prefix}:** {msg['text']}")
            st.divider()
    else:
        st.info("No messages yet." if not st.session_state.history else "No matches found.")

models = {
    "Groq": ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"],
    "OpenAI": ["gpt-4o-mini"],
}
provider = st.radio("Provider", list(models))
selected_model = st.selectbox("Model", models[provider])
allow_web_search = st.checkbox("Allow Web Search")
user_query = st.text_area("Your question", height=150, placeholder="Ask anything...")

API_URL = "http://127.0.0.1:8000/chat"

if st.button("Ask Agent!"):
    if not user_query.strip():
        st.warning("Enter a query first.")
    else:
        payload = {
            "model_name": selected_model,
            "model_provider": provider,
            "messages": [user_query],
            "allow_search": allow_web_search,
        }
        res = requests.post(API_URL, json=payload)
        if res.status_code != 200:
            st.error(f"Request failed: {res.status_code}")
        else:
            data = res.json() if res.headers.get("content-type", "").startswith("application/json") else res.text
            if isinstance(data, dict) and data.get("error"):
                st.error(data["error"])
            else:
                st.subheader("Agent response")
                st.write(data)
                st.session_state.history.append({"role": "user", "text": user_query})
                st.session_state.history.append({"role": "agent", "text": data})