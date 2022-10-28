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

def GetCanny(imgSrc, type, threshold1, threshold2, index=None):
	(imgDst)  = (None)

	wName  = 'GetCanny' + str(index)

	if(G.IS_DEBUG_GetCANNY):
		cv2.namedWindow(wName)
		cv2.createTrackbar('threshold1', wName, 0, 1000, OnTrackBarPass)
		cv2.setTrackbarPos('threshold1', wName, threshold1)	#300

		cv2.createTrackbar('threshold2', wName, 0, 1000, OnTrackBarPass)
		cv2.setTrackbarPos('threshold2', wName, threshold2)	#300

	while(True):
		imgRgbSrc = cv2.cvtColor(imgSrc, cv2.COLOR_GRAY2BGR)
		
		if(G.IS_DEBUG_GetCANNY):
			threshold1 =  cv2.getTrackbarPos('threshold1', wName)
			threshold2 =  cv2.getTrackbarPos('threshold2', wName)

		imgDst = cv2.Canny(imgSrc, threshold1, threshold2 )

		if(G.IS_DEBUG_GetCANNY):
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

	return (imgDst)

