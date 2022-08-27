#! /usr/bin/env python3.8

import cv2
import pdb
import numpy as np
from scipy import signal as sg
# import matplotlib.pyplot as plt
# import imag
import math
from os.path import join, dirname
from utils.Class import Color, Style

class Kernel:
	blur = np.ones((3, 3))/9
	egdes1 = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])

def saveCurFrame(frame, filename="capture.jpg"):
	_dir = dirname(__file__)

	cv2.imwrite(join(_dir, "dist/images", filename), cur_frame)	


# difference between 
# two images in 
# blur mode
IMG_DIFFERENCE = 800_000
IMG_DIFFERENCE_AVG = 2.60416667

# define a video capture object
vid = cv2.VideoCapture(0)

cur_frame = None
prev_frame = None

i = 0
while(True):
	ret, cur_frame = vid.read()

	if prev_frame is not None:
		img1 = cv2.cvtColor(cur_frame, cv2.COLOR_BGR2GRAY)
		img1 = sg.convolve2d(img1, Kernel.blur, mode="same", boundary="fill") 

		img2 = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
		img2 = sg.convolve2d(img2, Kernel.blur, mode="same", boundary="fill")

		diff = np.sum(abs(img1 - img2))
		diff_avg = diff/(img1.shape[0]*img1.shape[1])

		if diff_avg >= IMG_DIFFERENCE_AVG:
			print(Color.primary(f"[MOTION_DETECTOR]: motion {i + 1} detected"))
			saveCurFrame(cur_frame, f'capture{i}.jpg')
			i += 1

		# if diff >= IMG_DIFFERENCE:
		# 	print(i)

	# cv2.imshow('frame', cur_frame)

	prev_frame = cur_frame

	# the 'q' button is set as the
	# quitting button you may use any
	# desired button of your choice
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# After the loop release the cap object
vid.release()
cv2.destroyAllWindows()
