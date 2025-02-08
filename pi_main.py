from vision import AMXWebcam, Aggregator
import time, threading
# from network.pi_server import COORDINATES_BUFFER, run_server_threaded
import tkinter as tk
import numpy as np

root = tk.Tk()
root.title("Draw Dots")

# Create a canvas
canvas = tk.Canvas(root, width=800, height=800, bg="white")
canvas.pack()

POINTS_BUFFER = []
LAST_POINT = None

def draw_dot(x, y):
    """Draws a small dot at the clicked location while keeping previous dots."""
    if (0 <= x <= 800) and (0 <= y <= 800):
        dot_size = 3  # Size of the dot
        canvas.create_oval(x - dot_size, y - dot_size, x + dot_size, y + dot_size, fill="black", outline="black")

def draw_line(x, y):
    global LAST_POINT, POINTS_BUFFER
    if (0 <= x <= 800) and (0 <= y <= 800):
        POINTS_BUFFER.append((x, y))
    if len(POINTS_BUFFER) >= 3:
        new = np.mean(POINTS_BUFFER, axis=0)
        if LAST_POINT is not None:
            canvas.create_line(LAST_POINT[0], LAST_POINT[1], new[0], new[1], fill="black")
        LAST_POINT = new
        POINTS_BUFFER.clear()

if __name__ == '__main__':

    loop_time = 0.1
    cam1 = AMXWebcam(0, camera_location_vector=np.array([0.0, -210.0, 0.0]), camera_depth_vector=np.array([0.0, -1.0, 0.0]), camera_x_vector=np.array([-1.0, 0.0, 0.0]), camera_y_vector=np.array([0.0, 0.0, 1.0]))
    agg = Aggregator(cam1)

    while True:
        root.update()
        loop_start = time.time()
        # try:
        x1, y1, z1 = cam1.pos_estimate()
        print(x1, y1, z1)
        agg.add_data(cam1.pos_estimate())
        x, y, z = agg.get_estimate()
        # print(x, y, z)
        # COORDINATES_BUFFER.append((x, y, z))
        if (x, y, z) != (0.0, 0.0, 0.0):
            draw_line(800-z, -y+500)

        # except Exception as e:
        #     print(f"Exception encountered:\n{e}")
        loop_end = time.time()
        # print(loop_end - loop_start)
        if (loop_end - loop_start < loop_time):
            time.sleep(loop_time - (loop_end - loop_start))
