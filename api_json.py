from flask import Flask, request, jsonify
import vertexai, os
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel


app = Flask(__name__)

PROJECT_ID = "gemini-pro-video"
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)

"""API to summarize video"""
@app.route('/generate', methods=['POST'])
def generate_api():
    try:
        video_data = request.json['video_data']
        
        # video_part = Part.from_data(data=base64.b64decode(video_data), mime_type="video/mp4")
        video_part = generative_models.Part.from_uri(video_data, mime_type="video/mp4")
        
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

        for response in responses:
            text = response.candidates[0].content.parts[0].text
            generated_content_list.append(text)
            # print(text)
        
        print("Generated Content List:", generated_content_list)

        return jsonify({"generated_content": generated_content_list})
        # return jsonify(generated_content)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# local_file_path = "path/to/local/video.mp4"
# bucket_name = "your-bucket-name"
# destination_blob_name = "video.mp4"
# upload_video_to_bucket(local_file_path, bucket_name, destination_blob_name)
if __name__ == '__main__':
    app.run(debug=True)
