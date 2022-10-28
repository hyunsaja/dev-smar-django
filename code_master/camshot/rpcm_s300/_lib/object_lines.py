from logging.config import stopListening
import os
import sys
import glob
import cv2
import numpy as np

from pathlib import Path
from itertools import count
from tkinter.messagebox import NO
# from matplotlib import pyplot as plt
# from skimage import morphology
from logging import Filter
from functools import reduce

from . import _global_variable as G
from . import _utils as U
from . import _error_manager as EM


#roi
from . import roi as ROI

#Filter
from . import filter_bilateral as FB
from . import filter_threshold as FT
from . import filter_canny as FC

#Object
from . import object_components as compoObj
from . import object_contours as contoObj
from . import object_lines as lineObj

#Find Point
#from .  import _lib.find as F

def OnTrackBarPass(x):
	pass

def GetLines(imgSrc, type, length, group, index=None):
	(lines)  = (None)

	wName  = 'GetLines' + str(index)

	minLineLength = length if length<=255 else 255 	#200
	maxLineGap = group if group<=255 else 255		#300

	if(G.IS_DEBUG_GetLines):
		cv2.namedWindow(wName)

		cv2.createTrackbar('minLineLength', wName, 0, 255, OnTrackBarPass)
		cv2.setTrackbarPos('minLineLength', wName, minLineLength)

		cv2.createTrackbar('maxLineGap', wName, 0, 255, OnTrackBarPass)
		cv2.setTrackbarPos('maxLineGap', wName, maxLineGap)

	while(True):
		imgRgbSrc = cv2.cvtColor(imgSrc, cv2.COLOR_GRAY2BGR)
		
		if(G.IS_DEBUG_GetLines):
			minLineLength =  cv2.getTrackbarPos('minLineLength', wName)
			maxLineGap =  cv2.getTrackbarPos('maxLineGap', wName)

		lines = cv2.HoughLinesP(imgSrc, 1, np.pi/180, 10, None, minLineLength, maxLineGap)
		
		if lines is None:
			continue

		for line in lines:
			# 검출된 선 그리기
			x1, y1, x2, y2 = line[0]
			cv2.line(imgRgbSrc, (x1, y1), (x2, y2), G.COLOR_YELLOW, 1)

		if(G.IS_DEBUG_GetLines):
			imgRgbDst = cv2.cvtColor(imgSrc, cv2.COLOR_GRAY2BGR)
			resultImg = cv2.hconcat([imgRgbSrc, imgRgbDst])
			cv2.imshow(wName, resultImg)
			
			(wh, ww) = imgRgbDst.shape[:2]
			if ww * 2 <800:
				cv2.resizeWindow(wName, ww * 2  + 800, wh + 200)

			if cv2.waitKey(1) & 0xFF == 27:
				break
		else:
			break

	return (lines)
