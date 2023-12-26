from flask import Flask, request, jsonify
import vertexai
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel
from google.cloud import storage
import os
 
 
app = Flask(__name__)
 
PROJECT_ID = "gemini-pro-video"
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gemini-pro-video-0c248d500795.json"

"""function to upload a video file to a Google Cloud Storage bucket."""
def upload_video_to_bucket(local_file_path, bucket_name, destination_blob_name):
    storage_client = storage.Client()
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(local_file_path)
        cloud_uri = f"gs://{bucket_name}/{destination_blob_name}"
        print(f"File {local_file_path} uploaded to {cloud_uri}")
        return cloud_uri
    except Exception as e:
        print(f"Error uploading video to GCS: {str(e)}")
        return None
 
 
"""API to summarize video"""
@app.route('/generate_uri', methods=['POST'])
def generate_api():
    try:
        # Get the video URI from form-data
        video_data = request.files.get('video_data')
        print("video_data", video_data)

        file = None  # Initialize the variable outside the try block

        if video_data:
            # Save the file to a local path
            # dir_path = "D:/videos/"
            dir_path = "/app/"
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            local_file_path = os.path.join(dir_path, video_data.filename)
            video_data.save(local_file_path)
            print("local_file_path", local_file_path)
            # Upload the file to Google Cloud Storage
            try:
                file = upload_video_to_bucket(local_file_path, "cloud-ai-platform-749c2bf2-a41f-4b8b-9c48-01f94cfd4e45", video_data.filename)
            except Exception as e:
                print(f"Error uploading video to GCS: {str(e)}")

        else:
            return jsonify({"error": "No file received in the request"}), 400

        # Create a Part object from the video data
        video_part = generative_models.Part.from_uri(file, mime_type="video/mp4")
 
        model = GenerativeModel("gemini-pro-vision")
        responses = model.generate_content(
            [video_part.file_data.file_uri, """Analyze the video from a radiologist perspective. Also, provide a detailed summary as to possible abnormalities with explanation and suggestion if found"""],
            generation_config={
                "max_output_tokens": 2048,
                "temperature": 0.4,
                "top_p": 1,
                "top_k": 32
            },
            stream=True,
        )
 
        generated_content_list = []
        print("response: ", responses)
        
        for response in responses:
            text = response.candidates[0].content.parts[0].text
            print("text: ",text)
            generated_content_list.append(text)
 
        print("Generated Content List:", generated_content_list)
 
        return jsonify({"generated_content": generated_content_list})
 
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)