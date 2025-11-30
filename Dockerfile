FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit UI (users see the interface)
CMD ["streamlit", "run", "ui.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]