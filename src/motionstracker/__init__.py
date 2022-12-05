import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image
from scipy import signal as sg
from PIL import Image, ImageFilter
from os.path import join, dirname
import time
import os

try:
	from utils.Class import Color, Style
	from utils.variables import MODULE_NAME
except:
	from .utils.Class import Color, Style
	from .utils.variables import MODULE_NAME

class Kernel:
	blur = np.ones((3, 3))/9
	edges1 = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])

class MotionsTracker:
	def __init__(self, outputDirectory, outputFormat="images"):
		self.outputDirectory = outputDirectory
		self.MAX_IMGS_MATCH_DIST = 1850

		self.outputFormat = outputFormat

		if self.outputFormat != "video":
			self.outputFormat = "images"

	def run(self, duration=None, accuracy=1):
		"""
			@duration: duration of motions detection
						in second
			@accuracy: between 0 and 1

		"""

		if self.outputFormat == "video":
			self.runVideoCapture(duration, accuracy)
		else:
			self.runImagesCapture(duration, accuracy)

	def getVideoCaptureObject(self):
		# using front webcam

		for index in [0, 1, -1]:
			try: 
				vid = cv2.VideoCapture(index)

				# defile a video writer object
				ret, init_frame = vid.read()

				if ret:
					return vid
			except:
				pass

		print(Color.danger(f"[{MODULE_NAME.upper()}]: Pas de caméra accessible"))
		exit()

	def runImagesCapture(self, duration, accuracy):
		
		# define a video capture object
		vid = self.getVideoCaptureObject()

		cur_frame = None
		prev_frame = None


		# start time (s)
		t1 = time.time()

		i = 0
		while True:
			ret, cur_frame = vid.read()

			if prev_frame is not None and self.moving(cur_frame, prev_frame, accuracy):
					print(Color.primary(f"[{MODULE_NAME.upper()}]: motion {i + 1} detected"))
					
					# save the image
					t = time.time()
					self.saveCurrentFrame(cur_frame, f'motion-{i:03}-{t}.jpg', self.outputDirectory)

					i += 1

			prev_frame = cur_frame

			# get current time
			# and exit if time exceeded
			t2 = time.time()
			if duration != None and (t2 - t1) >= duration:
				break

		vid.release()


	def runVideoCapture(self, duration, accuracy):

		t = time.time()
		
		# define a video capture object
		vid = self.getVideoCaptureObject()

		# defile a video writer object
		ret, init_frame = vid.read()

		framesSize = (init_frame.shape[1], init_frame.shape[0])
		out = cv2.VideoWriter(
			join(self.outputDirectory, f'motions-video-{t}.avi'),
			cv2.VideoWriter_fourcc(*'DIVX'), 
			60, 
			framesSize
		)

		cur_frame = None
		prev_frame = None


		# start time (s)
		t1 = time.time()

		i = 0
		while True:
			ret, cur_frame = vid.read()

			if prev_frame is not None and self.moving(cur_frame, prev_frame, accuracy):
					print(Color.primary(f"[{MODULE_NAME.upper()}]: motion {i + 1} detected"))

					# write frame
					# for the video
					out.write(cur_frame)

					i += 1

			prev_frame = cur_frame

			# get current time
			# and exit if time exceeded
			t2 = time.time()
			if duration != None and (t2 - t1) >= duration:
				break
		
		vid.release()
		out.release()


	def moving(self, img1, img2, accuracy=1):
		if len(img1.shape) not in [1, 3] or len(img2.shape) not in [1, 3]:
			return

		if img1.shape != img2.shape:
			return

		img1 = self.prepareImage(img1)
		img2 = self.prepareImage(img2)

		# euclidian distance between img1 and img2
		dist = np.linalg.norm(img1 - img2)

		maxImgsDist = (2 - accuracy) * self.MAX_IMGS_MATCH_DIST 

		return dist >= maxImgsDist

	def saveCurrentFrame(self, frame, filename, target_dir):
		# save current frame {frame} as an image

		cv2.imwrite(join(target_dir, filename), frame)


	def prepareImage(self, img):
		if len(img.shape) == 3: #rgb
			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		img = sg.convolve2d(img, Kernel.blur, mode="same", boundary="fill")

		return img