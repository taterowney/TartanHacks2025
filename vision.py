import numpy as np
from convexhull import farthest_points_2d
import cv2

# WEBCAM DATASHEET: https://www.amx.com/en-US/product_documents/nmx-vcc-1000-datasheet-pdf

def filter_LED_color(image):
    """
    :param image: numpy array containing the image
    :return: the image with only the color of the LED, everything else filtered out
    """
    raise NotImplementedError("TODO")
    return np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)


def get_maximum_pixel_separation(filtered_image):
    """
    :param filtered_image: numpy array containing the image with only the LED color
    :return: points that are the farthest apart in the image
    """
    # Get points in image that are nonzero
    points = np.argwhere(filtered_image)
    p1, p2, _ = farthest_points_2d(points)
    return p1, p2

#TODO: maybe optimize this by just finding the mean of the extremal points?
def get_centroid(filtered_image):
    """
    :param filtered_image: numpy array containing the image with only the LED color
    :return: the centroid of the LED ring
    """
    points = np.argwhere(filtered_image)
    return np.mean(points, axis=0)


class Camera:
    """
    An abstract class for camera functions
    Should be subclassed for specific cameras, and have their attributes (sensor_width/height, image_width/height, focal_length) set
    """
    def __init__(self, camera_index, camera_location_vector=np.array([0.0, 100.0, 0.0]), camera_depth_vector=np.array([0.0, -1.0, 0.0]), camera_x_vector=np.array([-1.0, 0.0, 0.0]), camera_y_vector=np.array([0.0, 0.0, 1.0])):
        self.camera = cv2.VideoCapture(camera_index)

        # DEFAULT: at the top of the drawing surface 10cm away from the center, facing downwards towards the center of the paper
        self.camera_location_vector = camera_location_vector
        self.camera_coords_transform = np.linalg.inv(np.array([camera_x_vector / np.linalg.norm(camera_x_vector), camera_y_vector / np.linalg.norm(camera_y_vector), camera_depth_vector / np.linalg.norm(camera_depth_vector)]))

        self.pitch_x = self.sensor_width / self.image_width
        self.pitch_y = self.sensor_height / self.image_height

    def capture_image(self):
        ret, image = self.camera.read()
        if ret:
            return image
        else:
            return np.zeros((self.image_height, self.image_width, 3))

    def get_depth_mm(self, pt1, pt2, actual_separation=10):
        """
        Compute the distance on the sensor (in mm) for two points,
        taking into account separate horizontal/vertical pitches.

        ~ 0.003 ms per calculation
        """
        # Pixel deltas
        dx_px = pt2[0] - pt1[0]
        dy_px = pt2[1] - pt1[1]

        # Convert each axis separately
        dx_mm = dx_px * self.pitch_x
        dy_mm = dy_px * self.pitch_y

        # Euclidean distance on the sensor
        d_sensor_mm = np.sqrt(dx_mm ** 2 + dy_mm ** 2)

        return (self.focal_length * actual_separation) / d_sensor_mm

    def get_camera_coords(self, pt1, pt2, centroid):
        # TODO: numpy optimizations
        depth = self.get_depth_mm(pt1, pt2)
        lateral = centroid[0] - (self.image_width / 2)
        vertical = centroid[1] - (self.image_height / 2)
        return np.array([lateral, vertical, depth])

    def get_absolute_coords(self, pt1, pt2, centroid):
        """
        Get the absolute coordinates relative to the writing surface of the centroid of the LED ring
        :param pt1:
        :param pt2:
        :param centroid:
        :return: numpy array of [lateral distance from center of page, vertical distance from center of page, height above page]
        """
        camera_coords = self.get_camera_coords(pt1, pt2, centroid)
        return np.dot(self.camera_coords_transform, camera_coords) + self.camera_location_vector

    def pos_estimate(self):
        """
        :return: the estimated position of the LED ring
        """
        image = self.capture_image()
        # image = filter_LED_color(image)
        pt1, pt2 = get_maximum_pixel_separation(np.argwhere(image))
        return self.get_absolute_coords(pt1, pt2, np.mean([pt1, pt2], axis=0))


class CameraModule3(Camera):
    sensor_width = 3.68 # mm
    sensor_height = 6.45 # mm
    image_width = 2592 # pixels
    image_height = 4608 # pixels
    focal_length = 4.74 # mm

class AMXWebcam(Camera):

    image_width = 1920 # pixels
    image_height = 1080 # pixels


if __name__ == '__main__':
    cammod3 = CameraModule3(0)
    print(cammod3.pos_estimate())

