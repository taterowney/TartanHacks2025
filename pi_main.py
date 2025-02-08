from vision import AMXWebcam
import time, threading
# from network.pi_server import COORDINATES_BUFFER, run_server_threaded
import tkinter as tk

root = tk.Tk()
root.title("Draw Dots")

# Create a canvas
canvas = tk.Canvas(root, width=800, height=800, bg="white")
canvas.pack()

def draw_dot(x, y):
    """Draws a small dot at the clicked location while keeping previous dots."""
    if (0 <= x <= 800) and (0 <= y <= 800):
        dot_size = 3  # Size of the dot
        canvas.create_oval(x - dot_size, y - dot_size, x + dot_size, y + dot_size, fill="black", outline="black")

if __name__ == '__main__':
    # run_server_threaded()


    loop_time = 0.1
    cam1 = AMXWebcam(0)
    while True:
        root.update()
        loop_start = time.time()
        # try:
        x, y, z = cam1.pos_estimate()
        # COORDINATES_BUFFER.append((x, y, z))
        print(x, y, z)
        if (x, y, z) != (0.0, 0.0, 0.0):
            draw_dot(x-200, y+800)
        # except Exception as e:
        #     print(f"Exception encountered:\n{e}")
        loop_end = time.time()
        # print(loop_end - loop_start)
        if (loop_end - loop_start < loop_time):
            time.sleep(loop_time - (loop_end - loop_start))
