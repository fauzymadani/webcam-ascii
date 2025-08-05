import cv2
import os
import numpy as np
import time
import shutil

ASCII_CHARS = "@%#*+=-:. "

def frame_to_ascii(frame):
    terminal_size = shutil.get_terminal_size()
    term_width = terminal_size.columns
    term_height = terminal_size.lines - 1  

    height, width, _ = frame.shape
    aspect_ratio = height / width

    new_width = term_width
    new_height = int(aspect_ratio * new_width * 0.55)

    if new_height > term_height:
        new_height = term_height
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
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("cannot open webcam !")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            ascii_frame = frame_to_ascii(frame)
            clear_terminal()
            print(ascii_frame)
            time.sleep(0.03)  # ~30 FPS
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        clear_terminal()
        print("✌️ Webcam ASCII viewer exited.")

if __name__ == "__main__":
    main()

