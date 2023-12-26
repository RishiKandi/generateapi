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

# Copy the service account key file into the container
COPY gemini-pro-video-0c248d500795.json /app/gemini-pro-video-0c248d500795.json

# Set environment variables
ENV PATH="/google-cloud-sdk/bin:${PATH}"
ENV GOOGLE_APPLICATION_CREDENTIALS /app/gemini-pro-video-0c248d500795.json
ENV GCLOUD_PROJECT your-project-id

# Install any needed packages specified in requirements.txt
COPY api2.py .
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run api2.py when the container launches
CMD ["python", "api2.py", "run", "--host=0.0.0.0", "--port=5000"]
