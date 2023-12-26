from google.cloud import videointelligence 
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'C:/Users/sstgi/Downloads/video-408005-64062de5a3ec.json'

video_client = videointelligence.VideoIntelligenceServiceClient()
features = [videointelligence.Feature.OBJECT_TRACKING]
gcs_uri = "gs://bucketfor_video//MRI_5.mp4"
operation = video_client.annotate_video(
    request={"features": features, "input_uri": gcs_uri}
)
print("\nProcessing video for object annotations.")

result = operation.result(timeout=500)
print("\nFinished processing.\n")

# The first result is retrieved because a single video was processed.
object_annotations = result.annotation_results[0].object_annotations

for object_annotation in object_annotations:
    print("Entity description: {}".format(object_annotation.entity.description))
    if object_annotation.entity.entity_id:
        print("Entity id: {}".format(object_annotation.entity.entity_id))

    print(
        "Segment: {}s to {}s".format(
            object_annotation.segment.start_time_offset.seconds
            + object_annotation.segment.start_time_offset.microseconds / 1e6,
            object_annotation.segment.end_time_offset.seconds
            + object_annotation.segment.end_time_offset.microseconds / 1e6,
        )
    )

    print("Confidence: {}".format(object_annotation.confidence))

    # Here we print only the bounding box of the first frame in the segment
    frame = object_annotation.frames[0]
    box = frame.normalized_bounding_box
    print(
        "Time offset of the first frame: {}s".format(
            frame.time_offset.seconds + frame.time_offset.microseconds / 1e6
        )
    )
    print("Bounding box position:")
    print("\tleft  : {}".format(box.left))
    print("\ttop   : {}".format(box.top))
    print("\tright : {}".format(box.right))
    print("\tbottom: {}".format(box.bottom))
    print("\n")