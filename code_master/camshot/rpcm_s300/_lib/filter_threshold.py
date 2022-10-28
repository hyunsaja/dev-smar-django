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

def GetThreshold(imgSrc, type, threshold, max, index=None):
	(imgDst, thrsld)  = (None, threshold)

	wName  = 'GetThreshold' + str(index)

	if(G.IS_DEBUG_GetThreshold):
		cv2.namedWindow(wName)
		cv2.createTrackbar('threshold', wName, 0, 255, OnTrackBarPass)
		cv2.setTrackbarPos('threshold', wName, thrsld)

	while(True):
		imgRgbSrc = cv2.cvtColor(imgSrc, cv2.COLOR_GRAY2BGR)
		
		if(G.IS_DEBUG_GetThreshold):
			thrsld =  cv2.getTrackbarPos('threshold', wName)

		_, imgDst = cv2.threshold(imgSrc, thrsld, max, cv2.THRESH_BINARY)

		if(G.IS_DEBUG_GetThreshold):
			imgRgbDst = cv2.cvtColor(imgDst, cv2.COLOR_GRAY2BGR)
			resultImg = cv2.hconcat([imgRgbSrc, imgRgbDst])

			cv2.imshow(wName, resultImg)

			(wh, ww) = imgRgbDst.shape[:2]
			if ww * 2 <800:
				cv2.resizeWindow(wName, ww * 2  + 800, wh + 200)

			if cv2.waitKey(1) & 0xFF == 27:
				break
		else:
			break

	return (imgDst, thrsld)

