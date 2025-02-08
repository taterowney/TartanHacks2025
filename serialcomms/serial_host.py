import serial, time

"""
Conversation structure:

Raspberry Pi: waits in background
Host Computer: "ready"
Raspberry Pi: "|x,y,z|"
            ...(repeat as needed until execution terminates)...
Host Computer: "done"
"""

def parse_image_string(image_string):
    """
    :param image_string: string of the form "|x,y,z|"
    :return: tuple of (x, y, z)
    """
    camera_feeds = image_string.split('||')
    for camera_feed in camera_feeds:
        if camera_feed == '':
            continue
        try:
            x, y, z = camera_feed.split(',')
            return (float(x), float(y), float(z))
        except ValueError:
            return None

def host_mainloop(onreceive=lambda x: None, port='/dev/ttyACM0'):
    # Try to connect to the Pi on the provided serial port
    ser = None
    try:
        while not ser:
            try:
                ser = serial.Serial(port, 9600)
                break
            except serial.serialutil.SerialException:
                print(f"Unable to connect to serial port {port}. Retrying in 3s...")
                time.sleep(3)

        # Prompt the Pi to begin sending stuff
        ser.write(b'ready')
        print(f"Listening on port {port}...")
        while True:
            if ser.in_waiting:
                data = ser.readline().decode('utf-8').strip()
                onreceive(parse_image_string(data))
    except KeyboardInterrupt:
        pass
    finally:
        print("Exiting...")
        if ser:
            ser.write(b'done')
            ser.close()
