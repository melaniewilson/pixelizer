import cv2
import os
from tkinter import Tk, filedialog


def pixelate_frame(frame, pixelation_level):
    """
    Downscale and upscale a frame to achieve pixelation effect.

    Args:
        frame (numpy.ndarray): Input video frame.
        pixelation_level (int): Level of pixelation (lower = blockier).

    Returns:
        numpy.ndarray: Pixelated frame.
    """
    height, width = frame.shape[:2]
    temp_width = max(1, width // pixelation_level)
    temp_height = max(1, height // pixelation_level)

    # Resize down and then back up to original size
    temp = cv2.resize(frame, (temp_width, temp_height), interpolation=cv2.INTER_LINEAR)
    pixelated = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
    return pixelated


def pixelate_video(input_path, output_path, pixelation_level):
    """
    Process the video frame by frame and apply pixelation.

    Args:
        input_path (str): Path to the input .mp4 file.
        output_path (str): Path to save the pixelated output.
        pixelation_level (int): Amount of pixelation.
    """
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        print("❌ Error: Could not open video file.")
        return

    # Get original video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Set up video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    print(f"🎞️ Pixelating video... (level: {pixelation_level})")

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        pixelated = pixelate_frame(frame, pixelation_level)
        out.write(pixelated)
        frame_count += 1

    cap.release()
    out.release()
    print(f"✅ Done! Pixelated video saved as: {output_path} ({frame_count} frames processed)")


def get_user_input():
    """
    Open file dialogs for the user to select input video and output location,
    and ask for pixelation level.
    """
    Tk().withdraw()

    input_path = filedialog.askopenfilename(
        title="Select an MP4 video file",
        filetypes=[("MP4 files", "*.mp4")]
    )

    if not input_path:
        print("❌ No input file selected.")
        return None, None, None

    try:
        level = int(input("🔧 Enter pixelation level (e.g. 5 for chunky, 50 for mild): "))
        if level <= 0:
            raise ValueError
    except ValueError:
        print("❌ Invalid pixelation level. Please enter a positive integer.")
        return None, None, None

    output_path = filedialog.asksaveasfilename(
        title="Save Pixelated Video As...",
        defaultextension=".mp4",
        filetypes=[("MP4 files", "*.mp4")],
        initialfile="pixelized_output.mp4"
    )

    if not output_path:
        print("❌ No output location selected.")
        return None, None, None

    return input_path, output_path, level


if __name__ == "__main__":
    input_path, output_path, pixelation_level = get_user_input()

    if input_path and output_path and pixelation_level:
        pixelate_video(input_path, output_path, pixelation_level)
