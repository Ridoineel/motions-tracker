#! /usr/bin/env python3.8

import cv2
import numpy as np
from scipy import signal as sg
import math
from os.path import join, dirname
from utils.Class import Color, Style

# difference between 
# two images in 
# blur mode
IMG_DIFFERENCE = 800_000
IMG_DIFFERENCE_AVG = 2.60416667

class Kernel:
	blur = np.ones((3, 3))/9
	egdes1 = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])

def saveCurFrame(frame, filename="capture.jpg"):
	_dir = dirname(__file__)

	cv2.imwrite(join(_dir, "dist/images", filename), frame)	

def motion(img1, img2) -> bool:
	if len(img1.shape) not in [1, 3] or len(img2.shape) not in [1, 3]:
		return

	if len(img1.shape) == 3: #rgb
		img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

	if len(img2.shape) == 3: #rgb
		img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

	if img1.shape != img2.shape:
		return

	img1 = sg.convolve2d(img1, Kernel.blur, mode="same", boundary="fill") 
	img2 = sg.convolve2d(img2, Kernel.blur, mode="same", boundary="fill")

	diff = np.sum(abs(img1 - img2))
	diff_avg = diff/(img1.shape[0]*img1.shape[1])

	# return diff >= IMG_DIFFERENCE:

	return diff_avg >= IMG_DIFFERENCE_AVG

def main():
	# define a video capture object
	vid = cv2.VideoCapture(0)

	cur_frame = None
	prev_frame = None

	i = 0
	while(True):
		ret, cur_frame = vid.read()

		if prev_frame is not None and motion(cur_frame, prev_frame):
				print(Color.primary(f"[MOTION_DETECTOR]: motion {i + 1} detected"))
				saveCurFrame(cur_frame, f'capture{i}.jpg')
				i += 1

		# cv2.imshow('frame', cur_frame)

		prev_frame = cur_frame

		# the 'q' button is set as the
		# quitting button
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# After the loop release the cap object
	vid.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()
