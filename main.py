import cv2
import tkinter as tk
import tkinter.font as tkFont
import time

ASCII_CHARS = "@%#*+=-:. "

def frame_to_ascii(frame, width):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, original_width = gray.shape
    aspect_ratio = height / original_width

    new_height = int(aspect_ratio * width * 0.55)
    resized = cv2.resize(gray, (width, new_height))

    ascii_str = ""
    for row in resized:
        line = "".join(
            ASCII_CHARS[int(pixel) * len(ASCII_CHARS) // 256] for pixel in row
        )
        ascii_str += line.rstrip() + "\n"  
    return ascii_str

class AsciiWebcamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("idk")

        screen_width = 1366
        screen_height = 768
        window_width = int(screen_width * 0.75)
        window_height = int(screen_height * 0.75)
        self.root.geometry(f"470x380") # for small screen and if you want it to use alongside obs studio
        # self.root.geometry(f"{screen_width}x{screen_height}") # For a wider screen

        self.label = tk.Label(root, font=("Courier", 6), justify=tk.LEFT,
                              anchor="nw", bg="black", fg="white")
        self.label.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        self.font = tkFont.Font(family="Courier", size=6)
        self.char_width = self.font.measure("M")

        # Webcam
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("[ERR]: Failed to open webcam.")
            exit()

        self.device_name = "Default Webcam"
        self.fps = 0
        self.last_time = time.time()

        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            label_width_px = self.label.winfo_width()
            if label_width_px <= 1:
                label_width_px = 800  # fallback 

            ascii_width = max(10, int(label_width_px / self.char_width))

            ascii_art = frame_to_ascii(frame, width=ascii_width)

            # count for fps
            current_time = time.time()
            elapsed = current_time - self.last_time
            self.fps = 1 / elapsed if elapsed > 0 else 0
            self.last_time = current_time
            fps_cam = self.cap.get(cv2.CAP_PROP_FPS)

            header = f"Device: {self.device_name} | FPS: {fps_cam} | Loop FPS: {self.fps:.2f} | \n\n"
            self.label.config(text=header + ascii_art)

        self.root.after(30, self.update_frame)

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = AsciiWebcamApp(root)
    root.mainloop()

