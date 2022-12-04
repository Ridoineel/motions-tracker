import argparse
import cv2
import numpy as np
from matplotlib import image as Image
import os
import re
import datetime

def parser():
	parse = argparse.ArgumentParser()
	parse.add_argument("--output-dir", "-o", help="images | videos output directory", type=str)
	parse.add_argument("--accuracy", "-ac", help="motions accuracy", type=float)
	parse.add_argument("--duration", "-d", help="duration in second", type=str)
	parse.add_argument("--format", "-f", help="format of (images | video)", type=str)

	# parse.add_argument("--background", "-b", help="run in background", type=bool)

	parse.set_defaults(
		# background=False, 
		output_dir=".",
		accuracy=1,
		duration=None,
		format="images"
	)

	return parse.parse_args()

def parseTime(timeStr):
	""" parse string time from format 
			1m, 1s, 3h, 10:23 or 10:12:22 
		to seconds (int)

	"""

	time = None

	if re.match(r"^[0-9]{1,2}\:[0-9]{1,2}(\:[0-9]+)?$", timeStr) is not None:
		t = timeStr.split(":")

		hours = int(t[0])
		minutes = int(t[1])
		
		if len(t) == 3:
			seconds = int(t[2])
		else:
			seconds = 0

		time_delta = datetime.timedelta(seconds=seconds, minutes=minutes, hours=hours)
		time = time_delta.total_seconds()
	elif re.match(r"^[0-9]+(m|M)$", timeStr) is not None:
		minutes = int(timeStr[:-1])
		time = minutes * 60
	elif re.match(r"^[0-9]+(s|S)$", timeStr) is not None:
		seconds = int(timeStr[:-1])
		time = seconds
	elif re.match(r"^[0-9]+(h|H)$", timeStr) is not None:
		hours = int(timeStr[:-1])
		time = hours * 3600

	return time

def imgsToVideos():
	frameSize = (640, 480)

	out = cv2.VideoWriter('output_video.avi',cv2.VideoWriter_fourcc(*'DIVX'), 60, frameSize)

	nb_images = 100
	start = 0

	for i in range(start, start + nb_images):
		
		img = Image.imread(f"/home/ridoineel/Dev/motions-tracker/src/capture{i + 1}.jpg")
		out.write(img)

		os.system("clear")
		print(i+1)
		

		i += 1


	out.release()

if __name__ == '__main__':
	imgsToVideos()