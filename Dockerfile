# Use the official Python image from the Docker Hub for Windows
FROM python:3.11
# Set the working directory in the container
WORKDIR \app

# Copy the current directory contents into the container at C:\app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run api_json.py when the container launches
CMD ["python", "api_json.py", "-m", "flask", "run", "--host=0.0.0.0"]
