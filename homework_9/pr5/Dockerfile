# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the application
#CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0"]
CMD ["streamlit", "run", "main.py"]
