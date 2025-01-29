# train_model.py

# =======================
# 1. Import Required Libraries
# =======================
import cv2
import os
import shutil
import numpy as np
from keras.models import Model
from keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D
from keras.optimizers import Adam
from preprocess_video import extract_frames  # Import the frame extraction function
from concurrent.futures import ThreadPoolExecutor  # For multithreading

# =======================
# 2. Load and Preprocess a Single Image
# =======================
def load_and_preprocess_image(file_path):
    """
    Loads and preprocesses a single image.
    """
    img = cv2.imread(file_path)
    if img is not None:
        img = cv2.resize(img, (128, 128))  # Resize to match model input
        img = img / 255.0  # Normalize pixel values
    return img

# =======================
# 3. Load Images from Folder (Recursive with Multithreading)
# =======================
def load_images_from_folder_recursive(folder, max_workers=8):
    """
    Loads images from a folder and its subdirectories using multithreading.

    Parameters:
    - folder: Path to the folder containing images.
    - max_workers: Number of threads to use for loading images.
    """
    file_paths = []
    for root, _, files in os.walk(folder):
        for f in files:
            if f.endswith('.jpg'):  # Adjust to match your image format
                file_paths.append(os.path.join(root, f))

    # Use multithreading for faster image loading
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(load_and_preprocess_image, file_paths)

    # Filter out any None results (in case of failed reads)
    images = [img for img in results if img is not None]
    return np.array(images)

# =======================
# 4. Build the Convolutional Autoencoder
# =======================
def build_autoencoder():
    """
    Builds and compiles a convolutional autoencoder model.
    """
    input_img = Input(shape=(128, 128, 3))

    # Encoder
    x = Conv2D(32, (3, 3), activation='relu', padding='same')(input_img)
    x = MaxPooling2D((2, 2), padding='same')(x)
    x = Conv2D(16, (3, 3), activation='relu', padding='same')(x)
    encoded = MaxPooling2D((2, 2), padding='same')(x)

    # Decoder
    x = Conv2D(16, (3, 3), activation='relu', padding='same')(encoded)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
    x = UpSampling2D((2, 2))(x)
    decoded = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)

    autoencoder = Model(input_img, decoded)
    autoencoder.compile(optimizer=Adam(), loss='mse')
    return autoencoder

# =======================
# 5. Set Up Paths
# =======================
base_dir = os.path.dirname(os.path.dirname(__file__))

model_dir = os.path.join(base_dir, 'models')
data_dir = os.path.join(base_dir, 'data')
frames_dir = os.path.join(data_dir, 'frames')             # <-- Updated to data/frames
model_path = os.path.join(model_dir, 'anomaly_autoencoder.keras')
training_videos_folder = os.path.join(data_dir, 'training_videos')

os.makedirs(model_dir, exist_ok=True)
os.makedirs(data_dir, exist_ok=True)
os.makedirs(frames_dir, exist_ok=True)

# =======================
# 6. Train Autoencoder on Multiple Videos
# =======================
def train_autoencoder_on_multiple_videos(video_folder):
    """
    Loops through all video files in the folder, extracts frames,
    and trains the autoencoder on each video.
    """
    video_files = [f for f in os.listdir(video_folder) if f.endswith('.avi')]
    if not video_files:
        raise ValueError(f"No video files found in '{video_folder}'. Ensure there are .avi files.")

    for idx, video_file in enumerate(video_files, start=1):
        video_input_path = os.path.join(video_folder, video_file)
        print(f"Processing video: {video_input_path}")

        try:
            # Step 1: Extract frames to frames_dir
            extract_frames(video_input_path, frames_dir, idx)
            print(f"Frames extracted to '{frames_dir}' from video: {video_input_path}")

            # Step 2: Load frames
            data = load_images_from_folder_recursive(frames_dir)
            if len(data) == 0:
                raise ValueError(f"No frames loaded from '{frames_dir}' for video: {video_input_path}")

            # Step 3: Build and train the autoencoder
            autoencoder = build_autoencoder()
            autoencoder.fit(data, data, epochs=50, batch_size=32, validation_split=0.1)

            # Step 4: Save the trained model
            autoencoder.save(model_path)
            print(f"Model saved after training on video: '{video_input_path}'")

        except Exception as e:
            print(f"Error processing video '{video_input_path}': {e}")

        finally:
            # Clear frames directory to free up space
            shutil.rmtree(frames_dir)
            os.makedirs(frames_dir, exist_ok=True)
            print(f"Cleared frames directory for the next video.")

# =======================
# 7. Run the Training Process
# =======================
train_autoencoder_on_multiple_videos(training_videos_folder)
