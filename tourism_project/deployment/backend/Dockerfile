# Backend container: Flask API served with gunicorn
FROM python:3.9

# Set the working directory inside the container
WORKDIR /code

# Copy all backend files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start the API on port 7860, reachable on the Docker network
# -w 4        : 4 worker processes
# -b 0.0.0.0  : bind on all interfaces
# app:app     : run the Flask instance named `app` inside app.py
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:app"]
