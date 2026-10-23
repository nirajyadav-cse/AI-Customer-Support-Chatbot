import json
from datetime import datetime
from pathlib import Path
import pandas as pd
import streamlit as st
from chatbot import SupportChatbot, load_knowledge_base

st.set_page_config(page_title="Customer Support Chatbot", page_icon="💬", layout="wide")

@st.cache_resource
def get_bot():
    return SupportChatbot()

@st.cache_data
def get_kb():
    return load_knowledge_base()

bot = get_bot()
kb = get_kb()

st.title("💬 Customer Support Chatbot")
st.caption("A simple NLP-based support assistant with a knowledge base and human-escalation option.")

with st.sidebar:
    st.header("Support topics")
    st.write("📦 Orders and tracking")
    st.write("🚚 Shipping and delivery")
    st.write("↩️ Returns and refunds")
    st.write("💳 Payment questions")
    st.write("🔐 Account access")
    st.divider()
    st.caption("Demo project: do not enter passwords, card numbers, or other sensitive information.")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.escalations = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello! 👋 I'm your customer support assistant. Ask me about orders, delivery, returns, refunds, payments, or account access."
    }]
if "escalations" not in st.session_state:
    st.session_state.escalations = []

overview, chat_tab, knowledge_tab, escalation_tab = st.tabs(
    ["📊 Overview", "💬 Chat", "📚 Knowledge base", "🧑‍💼 Human support"]
)

with overview:
    user_messages = sum(1 for m in st.session_state.messages if m["role"] == "user")
    assistant_messages = sum(1 for m in st.session_state.messages if m["role"] == "assistant")
    escalated = len(st.session_state.escalations)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Knowledge articles", len(kb))
    m2.metric("Questions in this session", user_messages)
    m3.metric("Bot responses", assistant_messages)
    m4.metric("Escalation requests", escalated)
    st.subheader("What can I help with?")
    a, b, c = st.columns(3)
    a.info("📦 **Orders**\n\nTracking, address changes, cancellations")
    b.info("🚚 **Delivery**\n\nDelivery estimates and late packages")
    c.info("↩️ **Returns**\n\nReturn steps and refund status")
    d, e, f = st.columns(3)
    d.info("💳 **Payments**\n\nPayment methods and failed payments")
    e.info("🔐 **Accounts**\n\nPassword reset and account help")
    f.info("🧑‍💼 **Human support**\n\nEscalate questions the bot cannot answer")
    st.caption("Session metrics reset when the conversation is cleared or the app session ends.")

with chat_tab:
    st.subheader("Ask a support question")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("topic"):
                st.caption(f"Topic: {message['topic']}")
    prompt = st.chat_input("Type your question, e.g. How do I return an item?")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        result = bot.respond(prompt)
        st.session_state.messages.append({
            "role": "assistant", "content": result["answer"],
            "topic": result["topic"], "confidence": result["confidence"]
        })
        if result["escalate"]:
            st.session_state.escalations.append({
                "time": datetime.now().isoformat(timespec="seconds"),
                "question": prompt, "reason": "No sufficiently similar knowledge-base answer"
            })
        st.rerun()
    st.markdown("**Try asking:**")
    examples = ["How do I track my order?", "My payment failed", "When will I get my refund?"]
    cols = st.columns(len(examples))
    for col, example in zip(cols, examples):
        if col.button(example, use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": example})
            result = bot.respond(example)
            st.session_state.messages.append({"role": "assistant", "content": result["answer"], "topic": result["topic"]})
            if result["escalate"]:
                st.session_state.escalations.append({"time": datetime.now().isoformat(timespec="seconds"), "question": example, "reason": "No sufficiently similar knowledge-base answer"})
            st.rerun()

with knowledge_tab:
    st.subheader("Support knowledge base")
    category = st.selectbox("Filter category", ["All"] + sorted(kb["category"].unique().tolist()))
    shown = kb if category == "All" else kb[kb["category"] == category]
    st.dataframe(shown[["category", "question", "answer", "topic"]], use_container_width=True, hide_index=True)
    st.download_button("Download knowledge base CSV", kb.to_csv(index=False).encode("utf-8"), "knowledge_base.csv", "text/csv")

with escalation_tab:
    st.subheader("Contact human support")
    st.write("This educational demo records an escalation request in the current app session. It does not send a real email or create a real support ticket.")
    with st.form("support_form"):
        name = st.text_input("Your name (optional)")
        email = st.text_input("Email address (optional)")
        order_id = st.text_input("Order number (optional)")
        issue = st.text_area("Describe the issue", placeholder="Tell us what happened. Do not include passwords or full payment details.")
        submitted = st.form_submit_button("Record support request", type="primary")
        if submitted:
            if not issue.strip():
                st.warning("Please describe the issue before submitting.")
            else:
                ticket = {
                    "time": datetime.now().isoformat(timespec="seconds"),
                    "name": name.strip(), "email": email.strip(),
                    "order_id": order_id.strip(), "issue": issue.strip()
                }
                st.session_state.escalations.append(ticket)
                st.success("Demo request recorded for this session. In a production app, connect an approved ticketing system or secure backend.")
    if st.session_state.escalations:
        st.markdown("#### Requests recorded in this session")
        st.dataframe(pd.DataFrame(st.session_state.escalations), use_container_width=True, hide_index=True)
        st.download_button("Download session requests", pd.DataFrame(st.session_state.escalations).to_csv(index=False).encode("utf-8"), "support_requests.csv", "text/csv")
