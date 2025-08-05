import cv2
import os
import numpy as np
import time
import shutil

ASCII_CHARS = "@%#*+=-:. "

# frame handling
def frame_to_ascii(frame, max_width, max_height):
    height, width, _ = frame.shape
    aspect_ratio = height / width

    new_width = max_width
    new_height = int(aspect_ratio * new_width * 0.55)

    if new_height > max_height:
        new_height = max_height
        new_width = int(new_height / (aspect_ratio * 0.55))

    resized_frame = cv2.resize(frame, (new_width, new_height))
    gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

    ascii_str = ""
    for row in gray:
        for pixel in row:
            ascii_str += ASCII_CHARS[int(pixel) * len(ASCII_CHARS) // 256]
        ascii_str += "\n"

    return ascii_str

def clear_terminal():
    print("\033[H\033[J", end="")  

def main():
    device_path = "/dev/video0"
    cap = cv2.VideoCapture(device_path)

    if not cap.isOpened():
        print("Cannot open webcam!")
        return

    prev_time = time.time()
    frame_count = 0
    fps = 0

    try:
        while True:
            start_time = time.time()
            ret, frame = cap.read()
            if not ret:
                break

            term_size = shutil.get_terminal_size()
            term_width = term_size.columns
            term_height = term_size.lines - 2  # Sisakan 2 baris buat info

            ascii_frame = frame_to_ascii(frame, term_width, term_height)

            frame_count += 1
            current_time = time.time()
            if current_time - prev_time >= 1.0:
                fps = frame_count
                frame_count = 0
                prev_time = current_time

            clear_terminal()
            print(f"[FPS: {fps}] [Device: {device_path}]")
            print(ascii_frame)

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        clear_terminal()
        print("✌️ Webcam ASCII viewer exited.")

if __name__ == "__main__":
    main()

