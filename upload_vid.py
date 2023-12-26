from google.cloud import storage

"""function to upload a video file to a Google Cloud Storage bucket."""
def upload_video_to_bucket(local_file_path, bucket_name, destination_blob_name):
    storage_client = storage.Client()
    try:
        buckets = list(storage_client.list_buckets())
        print(buckets)
        bucket = storage_client.bucket("cloud-ai-platform-749c2bf2-a41f-4b8b-9c48-01f94cfd4e45")
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(local_file_path)
        print(f"File {local_file_path} uploaded to {bucket_name}/{destination_blob_name}")
    except Exception as e:
        print(f"Error uploading video to GCS: {str(e)}")


upload_video_to_bucket("D:/Swapnali/LLM/video/MRI_2.mp4", "cloud-ai-platform-749c2bf2-a41f-4b8b-9c48-01f94cfd4e45", "test_video")