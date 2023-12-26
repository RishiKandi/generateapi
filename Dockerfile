# Use a Debian base image with Python 3.8
FROM python:3.8-buster

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    curl

# Install Google Cloud SDK
RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-360.0.0-linux-x86_64.tar.gz && \
    tar -xzf google-cloud-sdk-360.0.0-linux-x86_64.tar.gz && \
    ./google-cloud-sdk/install.sh

# Set up gcloud configurations
RUN ./google-cloud-sdk/bin/gcloud init --quiet && \
    ./google-cloud-sdk/bin/gcloud auth application-default login --no-launch-browser --quiet && \
    ./google-cloud-sdk/bin/gcloud config set project your-project-id

# Set environment variables
ENV PATH="/google-cloud-sdk/bin:${PATH}"
ENV GOOGLE_APPLICATION_CREDENTIALS /app/gemini-pro-video-0c248d500795.json

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run api_json.py when the container launches
CMD ["python", "api_json.py", "run", "--host=0.0.0.0", "--port=5000"]
