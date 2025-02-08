from vision import *
import time
from network.pi_server import COORDINATES_BUFFER, run_server_threaded
if __name__ == '__main__':
    run_server_threaded()
    loop_time = 0.01
    while True:
        loop_start = time.time()
        try:
            x, y, z = (0, 0, 0)
            COORDINATES_BUFFER.append((x, y, z))
        except Exception as e:
            print(f"Exception encountered:\n{e}")
            continue
        loop_end = time.time()
        if (loop_end - loop_start < loop_time):
            time.sleep(loop_time - (loop_end - loop_start))
