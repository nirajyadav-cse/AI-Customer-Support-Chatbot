# AI Customer Support Chatbot

A beginner-friendly Artificial Intelligence project that answers common customer support questions using a searchable knowledge base and TF-IDF text similarity. It includes a Streamlit dashboard and an option to record a demo escalation request.

## 🚀 Live Demo

After deploying to Streamlit Community Cloud, replace the placeholder below with your app URL:



## Features

- Chat interface with conversation history for the current session.
- Knowledge-base matching for orders, delivery, returns, refunds, payments and account access.
- Dashboard metrics for articles, questions, responses and escalation requests.
- Searchable/filterable support knowledge base.
- Human-support escalation form (demo-only; does not send a real ticket).
- Downloadable knowledge base and session requests.

## Technologies

Python, Streamlit, pandas, scikit-learn, TF-IDF and cosine similarity.

## Project structure

```text
Customer_Support_Chatbot_AI_Project/
├── app.py
├── chatbot.py
├── requirements.txt
├── README.md
├── PROJECT_REPORT.md
└── data/
    └── knowledge_base.csv
```

## Run locally on macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL Streamlit prints, usually `http://localhost:8501`.

## How it works

1. A user asks a question.
2. TF-IDF converts the question and knowledge-base entries into vectors.
3. Cosine similarity finds the closest matching support question.
4. The chatbot returns the associated answer if the similarity score passes a threshold.
5. If no match is reliable enough, the chatbot recommends human support.

## Important limitations

This is a learning prototype, not a connected production support system. The chatbot does not access real orders, issue refunds, or send tickets. The knowledge base contains generic sample guidance; replace it with approved company-specific policies before real use. Do not submit passwords or full payment details.

## Future improvements

- Connect a secure helpdesk or ticketing system.
- Add authentication and safe order-status lookup.
- Add multilingual support and better semantic retrieval.
- Store anonymized analytics in a database with appropriate privacy controls.
- Test answer quality against a larger set of real, approved support questions.

## Author

Niraj Yadav — B.Tech CSE (AI & ML) student.
