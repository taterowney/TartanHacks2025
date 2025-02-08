import serial, time

def pi_mainloop(get_pen_location=lambda: (0, 0, 0), port='/dev/ttyACM0', loop_time=0.01):
    # run in a loop so that it will still function/reconnect even after it is disconnected
    ser = None
    while True:
        try:
            # Wait until the port is connected to the computer
            ser = None
            while not ser:
                try:
                    ser = serial.Serial(port, 9600)
                    break
                except serial.serialutil.SerialException:
                    print(f"Waiting for port {port} to connect. Retrying in 1s...")
                    time.sleep(1)

            print(f"Connected to port {port}. Waiting for 'ready' signal...")
            # Wait for computer to provide 'ready' signal
            while True:
                if ser.in_waiting:
                    data = ser.readline().decode('utf-8').strip()
                    if data == 'ready':
                        break

            print("Received 'ready' signal. Starting main loop...")
            # Transmit location every loop_time until the host says "done"
            while True:
                loop_start = time.time()
                try:
                    x, y, z = get_pen_location()
                except Exception as e:
                    print(f"Exception encountered:\n{e}")
                    continue
                ser.write(f'|{x},{y},{z}|'.encode('utf-8'))
                if ser.in_waiting:
                    data = ser.readline().decode('utf-8').strip()
                    if data == 'done':
                        break
                loop_end = time.time()
                if (loop_end - loop_start < loop_time):
                    time.sleep(loop_time - (loop_end - loop_start))

        # When the serial port is disconnected, default here, then loop back and wait for the port to connect again
        finally:
            if ser:
                ser.close()
