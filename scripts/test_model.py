# test_model.py

# =======================
# 1. Import Required Libraries
# =======================
import os
import cv2
import shutil
import numpy as np
from keras.models import load_model

from preprocess_video import extract_frames
from train_model import load_images_from_folder_recursive

from concurrent.futures import ThreadPoolExecutor, as_completed

# =======================
# 2. Set Up Paths
# =======================
base_dir = os.path.dirname(os.path.dirname(__file__))

data_dir = os.path.join(base_dir, 'data')
frames_dir = os.path.join(data_dir, 'frames')        # Now under data/frames
testing_videos_folder = os.path.join(data_dir, 'testing_videos')
results_dir = os.path.join(base_dir, 'results')

model_dir = os.path.join(base_dir, 'models')
model_path = os.path.join(model_dir, 'anomaly_autoencoder.keras')

os.makedirs(frames_dir, exist_ok=True)
os.makedirs(results_dir, exist_ok=True)

# =======================
# 3. Process Single Video
# =======================
def process_video(video_file, autoencoder, idx):
    video_input_path = os.path.join(testing_videos_folder, video_file)
    print(f"Processing video: {video_input_path}")

    # Unique subfolder for this video's frames
    video_frames_subdir = os.path.join(frames_dir, f"video_{idx}")
    os.makedirs(video_frames_subdir, exist_ok=True)

    try:
        # 1. Extract frames to a unique subfolder
        extract_frames(video_input_path, frames_dir, idx)
        # This creates frames in: data/frames/video_{idx}/frame_XXX.jpg

        # 2. Load frames (will resize + normalize to match training)
        data = load_images_from_folder_recursive(video_frames_subdir)
        if len(data) == 0:
            raise ValueError(f"No frames loaded from '{video_frames_subdir}' for video: {video_input_path}")

        # 3. Run predictions
        predictions = autoencoder.predict(data)

        # 4. Calculate reconstruction errors
        reconstruction_errors = np.mean((data - predictions) ** 2, axis=(1, 2, 3))

        # 5. Save results
        results_path = os.path.join(results_dir, f"results_video_{idx}.txt")
        with open(results_path, 'w') as f:
            for frame_idx, error in enumerate(reconstruction_errors):
                f.write(f"Frame {frame_idx}: Reconstruction Error = {error:.6f}\n")

        print(f"Results saved to '{results_path}'")

    except Exception as e:
        print(f"Error processing video '{video_input_path}': {e}")

    finally:
        # Clean up this video's frames
        if os.path.exists(video_frames_subdir):
            shutil.rmtree(video_frames_subdir)
            print(f"Cleared frames subdirectory: {video_frames_subdir}")


# =======================
# 4. Predict and Analyze Videos
# =======================
def test_autoencoder_on_videos(video_folder):
    video_files = [f for f in os.listdir(video_folder) if f.endswith('.avi')]
    if not video_files:
        raise ValueError(f"No video files found in '{video_folder}'. Ensure there are .avi files.")

    # Load the trained model
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Trained model not found at '{model_path}'. Train the model first.")
    autoencoder = load_model(model_path)
    print("Model loaded successfully.")

    # Multithreaded processing of each video
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(process_video, video_file, autoencoder, idx)
            for idx, video_file in enumerate(video_files, start=1)
        ]

        for future in as_completed(futures):
            try:
                future.result()  # Raise exceptions if any occurred
            except Exception as e:
                print(f"An error occurred during multithreaded processing: {e}")


# =======================
# 5. Main Execution
# =======================
if __name__ == "__main__":
    test_autoencoder_on_videos(testing_videos_folder)
