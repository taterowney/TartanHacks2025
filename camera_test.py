import cv2

def list_ports():
    """
    Test the ports and returns a tuple with the available ports and the ones that are working.
    """
    non_working_ports = []
    dev_port = 0
    working_ports = []
    available_ports = []
    while len(non_working_ports) < 6: # if there are more than 5 non working ports stop the testing.
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            non_working_ports.append(dev_port)
            print("Port %s is not working." %dev_port)
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                print("Port %s is working and reads images (%s x %s)" %(dev_port,h,w))
                working_ports.append(dev_port)
            else:
                print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
                available_ports.append(dev_port)
        dev_port +=1
    return available_ports,working_ports,non_working_ports

# list_ports()

cam1 = cv2.VideoCapture(1)
for i in range(10):
    while True:
        ret, image1 = cam1.read()
        height, width, channels = image1.shape
        image1[:height // 3, :, :] = 0
        cv2.imshow('Imagetest', image1)
        k = cv2.waitKey(1)
        if k != -1:
            break
    cv2.imwrite(f'testimage{i}.jpg', image1)

cam1.release()
