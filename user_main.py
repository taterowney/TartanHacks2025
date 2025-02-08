from network.user_client import get_coordinates
import time

if __name__ == '__main__':
    while 1:
        print(get_coordinates())
        time.sleep(0.25)
