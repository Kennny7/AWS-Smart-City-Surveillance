# preprocess_video.py
# =======================
# 1. Import Required Libraries
# =======================
import cv2
import os
from concurrent.futures import ThreadPoolExecutor  # For multithreading


# =======================
# 2. Save Frame Function (Used by Threads)
# =======================
def save_frame(frame, output_folder, frame_count):
    """
    Resizes and saves a video frame to the specified output folder.
    """
    try:
        frame = cv2.resize(frame, (128, 128))  # Resize frame to 128x128
        frame_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")  # Construct file path
        cv2.imwrite(frame_path, frame)  # Save frame as an image
    except Exception as e:
        print(f"Error saving frame {frame_count}: {e}")


# =======================
# 3. Extract Frames from Video with Multithreading
# =======================
def extract_frames(video_path, output_folder, video_index, frame_rate=1, max_workers=4):
    """
    Extracts frames from a video file and saves them to the output folder.

    Parameters:
    - video_path: Path to the input video file.
    - output_folder: Base folder where extracted frames will be saved.
    - video_index: Unique index for the video to avoid overwriting.
    - frame_rate: Extract every nth frame (default is 1, i.e., every frame).
    - max_workers: Number of threads to use for saving frames.
    """
    # Create a unique subfolder for each video
    video_folder = os.path.join(output_folder, f"video_{video_index}")
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Cannot open video file {video_path}")
        return

    frame_count = 0  # Counter for frames

    # Thread pool for concurrent frame saving
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        while cap.isOpened():
            try:
                ret, frame = cap.read()  # Read a frame
                if not ret:
                    break  # Break if video has ended or error occurs

                # Save frame at intervals defined by frame_rate
                if frame_count % frame_rate == 0:
                    executor.submit(save_frame, frame, video_folder, frame_count)

                frame_count += 1  # Increment frame counter
            except Exception as e:
                print(f"Error processing frame {frame_count}: {e}")

    # Release video capture object
    cap.release()
    print(f"Frames extracted for video {video_index} to '{video_folder}'")


# =======================
# 4. Batch Process Multiple Videos
# =======================
def process_videos(video_paths, output_folder, frame_rate=1, max_workers=4):
    """
    Processes multiple videos and extracts frames for each.

    Parameters:
    - video_paths: List of video file paths.
    - output_folder: Base folder where extracted frames will be saved.
    - frame_rate: Extract every nth frame (default is 1, i.e., every frame).
    - max_workers: Number of threads to use for saving frames.
    """
    for index, video_path in enumerate(video_paths, start=1):
        print(f"Processing video {index}: {video_path}")
        extract_frames(video_path, output_folder, index, frame_rate, max_workers)


# =======================
# 5. Example Usage
# =======================
# Example usage to process multiple videos
# video_list = ["video1.mp4", "video2.mp4", "video3.mp4"]
# process_videos(video_list, "frames", frame_rate=1, max_workers=4)
