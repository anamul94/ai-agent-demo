# ---- Base image ----
FROM python:3.12-slim

# ---- Install uv ----
RUN pip install uv

# ---- Set working directory ----
WORKDIR /app

# ---- Create virtual environment and install dependencies ----
RUN uv venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# ---- Copy requirements and install dependencies ----
COPY requirements.txt .
RUN uv pip install -r requirements.txt

# ---- Copy the rest of your app ----
COPY . .

# ---- Expose Streamlit port ----
EXPOSE 8501

# ---- Run Streamlit app ----
CMD ["streamlit", "run", "ui.py", "--server.port=8501", "--server.address=0.0.0.0"]