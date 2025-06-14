import cv2
import pytesseract
import yt_dlp
from PIL import Image
import numpy as np
import os

# Set Tesseract path (if not in system PATH)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows example


def download_youtube_video(url, output_dir="."):
    """Download a YouTube video using yt-dlp and return the file path."""
    try:
        ydl_opts = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
            "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
            "quiet": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            print(f"✅ Downloaded: {filename}")
            return filename
    except Exception as e:
        print(f"❌ Error downloading YouTube video: {e}")
        return None


def extract_frames(video_path, interval_sec=3):
    """Extract frames from a video at specified intervals."""
    print(f"📹 Extracting frames from {video_path}...")

    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise IOError(f"Could not open video: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            fps = 30  # Default assumption if FPS not detected
        print(f"🎞️ FPS: {fps}")

        interval = int(fps * interval_sec)
        print(f"⏱️ Extracting every {interval_sec} sec (~{interval} frames)")

        frames = []
        count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if count % interval == 0:
                frames.append(frame)
                # Optional: Save sample frames for debugging
                # cv2.imwrite(f"frame_{count}.jpg", frame)

            count += 1

        cap.release()
        print(f"📸 Extracted {len(frames)} frames.")
        return frames

    except Exception as e:
        print(f"❌ Error extracting frames: {e}")
        if "cap" in locals():
            cap.release()
        return []


def preprocess_frame(frame):
    """Improve OCR accuracy with preprocessing."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return threshold


def frame_to_text(frame):
    """Extract text from a frame using Tesseract OCR."""
    try:
        processed = preprocess_frame(frame)
        pil_img = Image.fromarray(processed)

        # Tesseract config (adjust as needed)
        custom_config = (
            r"--oem 3 --psm 6"  # OCR Engine Mode 3, Page Segmentation Mode 6
        )
        text = pytesseract.image_to_string(pil_img, config=custom_config)
        return text.strip()
    except Exception as e:
        print(f"⚠️ OCR Error: {e}")
        return ""


def save_text_to_file(text, filename="extracted_text.txt"):
    """Save extracted text to a file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"💾 Saved text to: {filename}")


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Replace with your YouTube URL
    YOUTUBE_URL = "https://www.youtube.com/watch?v=0z9_MhcYvcY"

    # 1. Download the video
    video_path = download_youtube_video(YOUTUBE_URL)

    if video_path and os.path.exists(video_path):
        # 2. Extract frames
        frames = extract_frames(
            video_path, interval_sec=3
        )  # Change interval_sec if needed

        if frames:
            # 3. Extract text from each frame
            extracted_texts = []
            for i, frame in enumerate(frames):
                text = frame_to_text(frame)
                if text:  # Only keep non-empty results
                    extracted_texts.append(f"🔹 Frame {i}:\n{text}\n{'-'*50}")

            # 4. Combine and save
            combined_text = "\n".join(extracted_texts)
            print("\n📝 Extracted Text:\n", combined_text)
            save_text_to_file(combined_text)

            # 5. Clean up (delete downloaded video)
            os.remove(video_path)
            print(f"🗑️ Deleted temporary video: {video_path}")
        else:
            print("❌ No frames extracted.")
    else:
        print("❌ Video download failed.")
