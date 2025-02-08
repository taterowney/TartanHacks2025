from vision import AMXWebcam
import time
# from network.pi_server import COORDINATES_BUFFER, run_server_threaded

if __name__ == '__main__':
    # run_server_threaded()
    loop_time = 0.01
    cam1 = AMXWebcam(0)
    while True:
        loop_start = time.time()
        # try:
        x, y, z = cam1.pos_estimate()
        # COORDINATES_BUFFER.append((x, y, z))
        print(x, y, z)
        # except Exception as e:
        #     print(f"Exception encountered:\n{e}")
        loop_end = time.time()
        print(loop_end - loop_start)
        if (loop_end - loop_start < loop_time):
            time.sleep(loop_time - (loop_end - loop_start))
