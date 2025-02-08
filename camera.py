# Have ported everything from here to vision.py

import cv2


cam1 = cv2.VideoCapture(0)
# cam2 = cv2.VideoCapture(1)

while True:
	ret, image1 = cam1.read()
	# ret2, image2 = cam2.read()
	cv2.imshow('Imagetest', image1)
	k = cv2.waitKey(1)
	if k != -1:
		break
	# cv2.imshow('Imagetest',image2)
	# k = cv2.waitKey(1)
	# if k != -1:
	# 	break

cv2.imwrite('/home/pi/testimage.jpg', image1)
cam1.release()
# cv2.imwrite('/home/pi/testimage.jpg', image2)
# cam2.release()
cv2.destroyAllWindows()