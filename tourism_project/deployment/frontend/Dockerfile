# Frontend container: Streamlit UI
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy all frontend files into the container
COPY . .

# Install dependencies
RUN pip3 install -r requirements.txt

# Run the Streamlit app on port 8501, reachable externally
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false"]
