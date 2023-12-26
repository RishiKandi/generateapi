from google.cloud import videointelligence 
import os, io


"""Detects camera shot changes."""
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'C:/Users/sstgi/Downloads/video-408005-64062de5a3ec.json'
path = "C:\\Users\\sstgi\\Downloads\\MRI_5.mp4"
video_client = videointelligence.VideoIntelligenceServiceClient()
features = [videointelligence.Feature.SHOT_CHANGE_DETECTION]
operation = video_client.annotate_video(
    request={"features": features, "input_uri": path}
)
print("\nProcessing video for shot change annotations:")

result = operation.result(timeout=90)
print("\nFinished processing.")

# first result is retrieved because a single video was processed
for i, shot in enumerate(result.annotation_results[0].shot_annotations):
    start_time = (
        shot.start_time_offset.seconds + shot.start_time_offset.microseconds / 1e6
    )
    end_time = (
        shot.end_time_offset.seconds + shot.end_time_offset.microseconds / 1e6
    )
    print("\tShot {}: {} to {}".format(i, start_time, end_time))