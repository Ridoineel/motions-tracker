#! /usr/bin/env python3.8

from os.path import join, dirname, isdir
import datetime


try:
	from __init__ import MotionsTracker
	from utils.functions import *
	from utils.Class import Color, Style
	from utils.variables import MODULE_NAME
except:
	from .__init__ import MotionsTracker
	from .utils.functions import *
	from .utils.Class import Color, Style
	from .utils.variables import MODULE_NAME

def main():
	data = parser()

	accuracy = data.accuracy
	outputDirectory = data.output_dir
	outputFormat = data.format
	duration = data.duration

	if not isdir(outputDirectory):
		print(Color.danger(f"[{MODULE_NAME}]: {outputDirectory} is not a directory"))
		exit()

	if duration != None:
		duration = parseTime(duration)

		if duration == None:
			print(Color.danger(f"[{MODULE_NAME}]: Incorrect duration format; only 1m, 13h, 3s, 11:22:11 or 11:11"))
			exit()

	motionsTracker = MotionsTracker(outputDirectory, outputFormat)
	motionsTracker.run(duration, accuracy)

if __name__ == "__main__":
	main()
