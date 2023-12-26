import streamlit as st

import io, os

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'C:/Users/sstgi/Downloads/video-408005-64062de5a3ec.json'

# Create Video Intelligence client


# Function to process video and display results
def process_video_and_display_results(video_path):
    from google.cloud import videointelligence 
    video_client = videointelligence.VideoIntelligenceServiceClient()
    # Read video content
    with io.open(video_path, "rb") as movie:
        input_content = movie.read()

    # Annotate video
    operation = video_client.annotate_video(
        request={"features": [videointelligence.Feature.LABEL_DETECTION], "input_content": input_content}
    )

    # Wait for annotation operation to complete
    result = operation.result(timeout=90)

    # Process video/segment level label annotations
    segment_labels = result.annotation_results[0].segment_label_annotations
    max_confidence_segment = max(segment_labels, key=lambda x: x.segments[0].confidence)

    # Display results in Streamlit
    st.write("\nProcessing video for label annotations....")
    st.write("\nFinished processing.")
    st.write("Video label description: {}".format(max_confidence_segment.entity.description))
    st.write("\tCategory description: {}".format(max_confidence_segment.category_entities[0].description))
    st.write("\tConfidence: {}".format(max_confidence_segment.segments[0].confidence))

# Streamlit app
def main():
    st.title("Video Annotation with Google API")

    # File uploader
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4"])

    if uploaded_file is not None:
        # Display video details
        st.video(uploaded_file)

        # Process the uploaded video and display results
        process_video_and_display_results(uploaded_file)

if __name__ == "__main__":
    main()
