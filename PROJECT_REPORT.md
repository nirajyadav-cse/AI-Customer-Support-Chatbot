# Project Report: AI Chatbot for Customer Support

## 1. Introduction
Customer support teams handle repeated questions about orders, delivery, returns, payments and accounts. A chatbot can answer common questions quickly and direct uncertain cases to a human representative.

## 2. Problem statement
Develop an AI-powered chatbot prototype that matches customer questions to a prepared support knowledge base, returns relevant guidance and offers a human-support escalation path.

## 3. Objectives
1. Create a support knowledge base.
2. Process questions with basic NLP.
3. Retrieve the most similar known question.
4. Display answers in a chat interface.
5. Show dashboard metrics and allow knowledge-base exploration.
6. Record demo escalation requests.

## 4. Technologies
Python, Streamlit, pandas, scikit-learn, TF-IDF vectorization and cosine similarity.

## 5. System methodology
**Input:** The customer types a support question.

**Vectorization:** TF-IDF converts the question and knowledge-base text into numerical vectors.

**Retrieval:** Cosine similarity compares the query against stored questions and topics.

**Response:** If the best match passes a chosen threshold, the associated answer is returned. Otherwise, the chatbot recommends human support.

**Dashboard:** Streamlit displays conversation history, session metrics, support articles and an escalation form.

## 6. Knowledge base
The included CSV contains example answers for orders, shipping, returns, payments, account access and general questions. It is demonstration content and should be replaced with approved business policies for real deployment.

## 7. Human escalation
The form records a request in the active Streamlit session and permits downloading it as a CSV. It does not send email or create a real ticket. A production implementation needs a secure, authorized backend or ticketing integration.

## 8. Testing plan
- Ask a question similar to a known knowledge-base entry and verify a relevant answer.
- Ask an unrelated question and verify that human support is suggested.
- Check category filters and CSV download.
- Submit an escalation form with an empty issue and verify validation.
- Submit a valid demo request and check the session table.

## 9. Limitations
TF-IDF similarity is lexical and may fail to understand paraphrases, complex multi-part questions, context or intent. The app has no real order-system integration and no persistent ticket storage.

## 10. Future scope
Use semantic embeddings, add a larger approved knowledge base, integrate a real helpdesk, secure customer identity verification, support multiple languages and evaluate answer quality with test questions.

## 11. Conclusion
This project demonstrates an introductory customer-support chatbot with NLP-based retrieval, a web chat interface, knowledge-base analytics and a human-escalation prototype.
