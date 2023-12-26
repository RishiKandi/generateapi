import cv2
import os

def convert_video_to_frames(video_path, output_path, frame_limit=None):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Read the video frame by frame
    frame_count = 0
    while True:
        ret, frame = cap.read()

        if not ret or (frame_limit is not None and frame_count >= frame_limit):
            break

        # Save the frame as an image
        frame_filename = os.path.join(output_path, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(frame_filename, frame)

        frame_count += 1

    # Release the video capture object
    cap.release()

    print(f"Frames extracted: {frame_count}")

# Example usage with a frame limit of 100
video_path = r"C:\Users\sstgi\Downloads\MRI_5.mp4"
output_directory = r"D:\Swapnali\LLM\video\output_frames"
frame_limit = 100

convert_video_to_frames(video_path, output_directory, frame_limit)
