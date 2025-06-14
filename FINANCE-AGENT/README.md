# Finance Agent
## Description
It will provide financial insights and recommendations based on user input.
## Prerequisites
- Provide Groq[https://groq.com] API key in .env file
- 
## Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run ui.py
```
## Docker
```bash
docker build -t yt-summarizer .
docker run --env-file .env -p 8501:8501 yt-summarizer
```
