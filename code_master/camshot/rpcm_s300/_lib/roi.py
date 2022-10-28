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


def GetUserROI(imgSrc, type, realW, index=None):
	print(type, realW, index)
	(imgRoi, (x_, y_, w_, h_))  = (None, (0, 0, 0, 0))

	w_ = G.ROI_WIDTH
	h_ = int(float(realW) / G.PIX2MM[type])

	x_ = G.ROI_X_BASE[type]
	y_ = G.ROI_Y_BASE[type] - h_
	
	imgRoi = imgSrc[y_: y_ + h_, x_ : x_ + w_]
	return (imgRoi, (x_, y_, w_, h_)) 


def GetAutoROI(imgSrc, type, x, y, w, h, index=None):
	(imgRoi, sortListStats, (x_, y_, w_, h_), threshold)  = (None, None, (0, 0, 0, 0), 0)

	wName  = 'GetAutoROI' + str(index)

	#filter Bilateral
	sigmaColor = 10
	sigmaSpace = 5
	imgRoi = FB.GetBilateral(imgSrc, type, sigmaColor, sigmaSpace, index)


	#filter Threshold
	max = imgSrc.max()
	mean = np.mean(imgSrc)
	threshold = int(mean * G.THRESHOLD_RATE[type])
	if threshold>=255 and mean<=100:
		threshold = 200
	elif threshold>=255 and mean>=100:
		threshold = 253
	(imgRoi, threshold) = FT.GetThreshold(imgRoi, type, threshold, max, index)


	#Get GetComponentStats
	sortKey = G.COMPONENTS_SORT_KEY['h']
	#sortKey = G.COMPONENTS_SORT_KEY['area']
	sortListStats = compoObj.GetComponentStats(imgRoi, type, sortKey, index)
	(x_, y_, w_, h_, _) = sortListStats[1]	#가장 큰놈
	
	# >>> delete small components ----------
	for status in sortListStats:
		(x__, y__, w__, h__, area__) = status
		if area__ < G.COMPONENTS_AREA_REMOVE[type]:
			sortListStats.remove(status)
			imgRoi = cv2.rectangle(imgRoi, (x__, y__), (x__ + w__, y__ + h__), G.COLOR_BLACK, -1)
	# <<< delete small components ----------

	imgRoi = imgRoi[y_: y_ + h_, x_ : x_ + w_]
	return (imgRoi, sortListStats, (x_, y_, w_, h_), threshold) 


def SetFitROI(imgSrc, _TYPE, x, y, w, h, index=None):
	(imgRoi, (x_, y_, w_, h_))  = (None, (0, 0, 0, 0))

	# [가로 라인 삭제]
	#1. 원본 gray(배경 흰색, 객체 검정)
	#2. Canny
	#3. HoughLinesP minLineLength=20, maxLineGap=int(_w*2/3)
	#4. x축에 평행한 선 찾아서
	#5. 바로 윗 줄의 5픽셀정도 복사해서 해당선 위 상단에 붙여넣기
	#6. 바로 아랫 줄의 5픽셀정도 복사해서 해당선 위 하단에 붙여넣기
	#
	# *** 크로스 빔에서 일자 빔으로 바꿔서 위 개발 취소

	return (imgRoi, (x_, y_, w_, h_))

