from google.cloud import videointelligence 
import os, io

"""This API provides following services:
    1. authenticate to the API
    2. analyzing videos for labels
    3. detect faces
    4. detect people
    5. detect shot changes
    6. detect explicit content
    7. track object
    8. recognize logos
    9. transcribe speech 
"""
"""Detect labels given a file path."""
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'C:/Users/sstgi/Downloads/video-408005-64062de5a3ec.json'
video_client = videointelligence.VideoIntelligenceServiceClient()
features = [videointelligence.Feature.LABEL_DETECTION]
path = "C:\\Users\\sstgi\\Downloads\\MRI_5.mp4"

with io.open(path, "rb") as movie:
    input_content = movie.read()
operation = video_client.annotate_video(
    request={"features": features, "input_content": input_content}
)
print("\nProcessing video for label annotations....")
result = operation.result(timeout=90)
print("\nFinished processing.")
# print("result annotation: ", result.annotation_results[0])

# Process video/segment level label annotations
segment_labels = result.annotation_results[0].segment_label_annotations
max_confidence_segment = max(segment_labels, key=lambda x: x.segments[0].confidence)
print("Video label description: {}".format(max_confidence_segment.entity.description))
print("\tCategory description: {}".format(max_confidence_segment.category_entities[0].description))
print("\tConfidence: {}".format(max_confidence_segment.segments[0].confidence))

"""
# Process shot level label annotations
shot_labels = result.annotation_results[0].shot_label_annotations
max_confidence_label = max(shot_labels, key=lambda x: x.segments[0].confidence)
print("Shot label description: {}".format(max_confidence_label.entity.description))
print("\tCategory description: {}".format(max_confidence_label.category_entities[0].description))
print("\tConfidence: {}".format(max_confidence_label.segments[0].confidence))

# Process frame level label annotations
frame_labels = result.annotation_results[0].frame_label_annotations
if frame_labels:
    max_confidence_frame = max(frame_labels, key = lambda x: x.segments[0].confidence)
    print("Frame label description: {}".format(max_confidence_frame.entity.description))
    print("\tCategory description: {}".format(max_confidence_frame.category_entities[0].description))
    print("\tConfidence: {}".format(max_confidence_frame.segments[0].confidence))

"""