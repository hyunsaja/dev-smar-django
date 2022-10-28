
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

class MyClass:

	# >>> Function ----------
	def GetPointCH(data):
		#Return Format
		(dst,(topX, topY, middleX, middleY, bottomX, bottomY)) = (None,(0, 0, 0, 0, 0, 0))

		#주석을 하면 실행
		#return (MyClass._ERROR_CODE, dst,(topX, topY, middleX, middleY, bottomX, bottomY))

		# >>> ROI ----------
		(imgRoi, (x_, y_, w_, h_)) = ROI.GetUserROI(
			MyClass._IMG_SRC.copy(), MyClass._TYPE, MyClass._WEB, MyClass._INDEX)
		(x, y, w, h) = (x_, y_, w_, h_)
		#cv2.rectangle(MyClass._IMG_RGB_DSC, (x, y), (x+w-1, y+h-1), G.COLOR_RED, 1)
		#cv2.imshow('ch' + str(MyClass._INDEX), MyClass._IMG_RGB_DSC)
		

		#실 사용할 imgRoi, threshold
		(imgRoi, sortListStats, (x_, y_, w_, h_), threshold) = ROI.GetAutoROI(
			imgRoi.copy(), MyClass._TYPE, x, y, w, h, MyClass._INDEX)
		(x, y, w, h) = (x+x_, y+y_, w_, h_)
		#cv2.rectangle(MyClass._IMG_RGB_DSC, (x, y), (x+w-1, y+h-1), G.COLOR_GREEN, 1)
		#cv2.imshow('ch' + str(MyClass._INDEX), MyClass._IMG_RGB_DSC)

		
		# 사용하지 않음 [가로 라인 삭제]
		#(imgRoi, (x_, y_, w_, h_)) = ROI.SetFitROI(
		#	imgRoi.copy(), MyClass._TYPE, x, y, w, h, MyClass._INDEX)
		#(x, y, w, h) = (x+x_, y+y_, w_, h_)
		# <<< ROI ----------


		# >>> GET END POINT ----------
		(sortListContours, hier) = contoObj.GetContours(imgRoi.copy(), MyClass._TYPE, MyClass._INDEX)
		(area, contr) = sortListContours[0]

		# 중심점 통과하는 직선 표시
		# https://jwmath.tistory.com/493
		[vx, vy, x__, y__] = cv2.fitLine(contr, cv2.DIST_L2, 0, 0.01, 0.01)
		rows, cols = imgRoi.shape[:2]

		y11 = 0
		x11 = (vx/vy)*(0-y__)+x__
		y12 = rows
		x12 = (vx/vy)*(rows-y__)+x__

		cv2.line(MyClass._IMG_RGB_DSC, (int(x11+x), int(y11+y)), (int(x12+x), int(y12+y)), G.COLOR_GREEN, 2)

		cv2.circle(MyClass._IMG_RGB_DSC, (int(x11+x), int(y11+y)), 5, G.COLOR_RED, 2)
		cv2.circle(MyClass._IMG_RGB_DSC, (int(x12+x), int(y12+y)), 5, G.COLOR_RED, 2)
		# <<< GET END POINT ----------


		# <<< GET MIDDLE POINT ----------
		x21 = 0
		y21 = y11 + int(abs(y12-y11)/2)
		x22 = 100
		y22 = y21

		(cx, cy) = U.GetCrossPoint(x11, y11, x12, y12,	x21, y21, x22, y22)

		cv2.circle(MyClass._IMG_RGB_DSC, (int(cx+x), int(cy+y)), 5, G.COLOR_RED, 2)
		#cv2.imshow('ch' + str(MyClass._INDEX), MyClass._IMG_RGB_DSC)
		
		# >>> GET MIDDLE POINT ----------

		topX, topY = int(x11+x), int(y11+y)
		middleX, middleY = int(cx+x), int(cy+y)
		bottomX, bottomY = int(x12+x), int(y12+y)

		dst = MyClass._IMG_RGB_DSC[y-G.RESULT_MARGIN: y + h_ + G.RESULT_MARGIN*2, x-G.RESULT_MARGIN : x + w_+G.RESULT_MARGIN*2]

		return (MyClass._ERROR_CODE, dst,(topX, topY, middleX, middleY, bottomX, bottomY))

	def GetPointEA(data):

		#Return Format
		(dst,(topX, topY, middleX, middleY, bottomX, bottomY)) = (None,(0, 0, 0, 0, 0, 0))

		#주석을 하며 실행
		#return (MyClass._ERROR_CODE, dst,(topX, topY, middleX, middleY, bottomX, bottomY))
		print(data)
		# >>> ROI ----------
		(imgRoi, (x_, y_, w_, h_)) = ROI.GetUserROI(
			MyClass._IMG_SRC.copy(), MyClass._TYPE, MyClass._WEB, MyClass._INDEX)
		(x, y, w, h) = (x_, y_, w_, h_)
		print('3')
		#cv2.rectangle(MyClass._IMG_RGB_DSC, (x, y), (x+w-1, y+h-1), G.COLOR_RED, 1)
		#cv2.imshow('ea' + str(MyClass._INDEX), MyClass._IMG_RGB_DSC)
		

		#실 사용할 imgRoi, threshold
		(imgRoi, sortListStats, (x_, y_, w_, h_), threshold) = ROI.GetAutoROI(
			imgRoi.copy(), MyClass._TYPE, x, y, w, h, MyClass._INDEX)
		(x, y, w, h) = (x+x_, y+y_, w_, h_)
		#cv2.rectangle(MyClass._IMG_RGB_DSC, (x, y), (x+w-1, y+h-1), G.COLOR_GREEN, 1)
		#cv2.imshow('ea' + str(MyClass._INDEX), MyClass._IMG_RGB_DSC)
		print('4')

		
		# 사용하지 않음 [가로 라인 삭제]
		#(imgRoi, (x_, y_, w_, h_)) = ROI.SetFitROI(
		#	imgRoi.copy(), MyClass._TYPE, x, y, w, h, MyClass._INDEX)
		#(x, y, w, h) = (x+x_, y+y_, w_, h_)
		# <<< ROI ----------



		# >>> GET LINE ----------
		imgRoi = MyClass._IMG_SRC[y: y + h, x : x + w]

		threshold1 = 300
		threshold2 = 300
		imgRoi = FC.GetCanny(imgRoi, MyClass._TYPE, threshold1, threshold2, MyClass._INDEX)
		print('5')

		length = int(imgRoi.shape[0] * 1/3)
		group = int(imgRoi.shape[0])
		lines = lineObj.GetLines(imgRoi, MyClass._TYPE, length, group, MyClass._INDEX)
		imgRgbRoi = cv2.cvtColor(imgRoi, cv2.COLOR_GRAY2BGR)
		print('6')

		if lines is None:
			
			return (MyClass._ERROR_CODE, dst,(topX, topY, middleX, middleY, bottomX, bottomY))

		m = sys.maxsize
		listPositiveLines = []
		listNegativeLines = []
		for line in lines:
			(x1, y1, x2, y2) = line[0]
			l = (x1, y1, x2, y2)

			if (y2==y1): #수평
				m=0
				pass
			elif (x2==x1): #수직
				pass
			else:
				m = (y2-y1)/(x2-x1)

			if m>0:
				listPositiveLines.append(l)
			else:
				listNegativeLines.append(l)
				
		#https://steadiness-193.tistory.com/46
		#positiveLines = np.average(listPositiveLines, axis=0)
		positiveLines = np.mean(listPositiveLines, axis=0)
		#negativeLines = np.average(listNegativeLines, axis=0)
		negativeLines = np.mean(listNegativeLines, axis=0)
		# <<< GET LINE ----------


		# >>> GET END POINT ----------
		(ha, wa) = imgRoi.shape[:3]

		(x11, y11, x12, y12) = positiveLines
		(x21, y21, x22, y22) = (0, 0, G.LINE_THICKNESS, 0) #top line

		(sx, sy) = U.GetCrossPoint(x11, y11, x12, y12,	x21, y21, x22, y22)

		cv2.line(MyClass._IMG_RGB_DSC, (int(sx)+x, int(sy)+y), (int(x12)+x, int(y12)+y), G.COLOR_YELLOW, 1)
		cv2.circle(MyClass._IMG_RGB_DSC, (int(sx)+x, int(sy)+y), 5, G.COLOR_RED, 2)

		#------------------------------

		(x21, y21, x22, y22) = negativeLines
		(x11, y11, x12, y12) = (0, ha, G.LINE_THICKNESS, ha) #bottom line

		(ex, ey) = U.GetCrossPoint(x11, y11, x12, y12,	x21, y21, x22, y22)

		cv2.line(MyClass._IMG_RGB_DSC, (int(ex)+x, int(ey)+y), (int(x22)+x, int(y22)+y), G.COLOR_YELLOW, 1)
		cv2.circle(MyClass._IMG_RGB_DSC, (int(ex)+x, int(ey)+y), 5, G.COLOR_RED, 2)
		# <<< GET END POINT ----------


		# >>> GET MIDDLE POINT ----------
		(x11, y11, x12, y12) = positiveLines
		(x21, y21, x22, y22) = negativeLines
		(cx, cy) = U.GetCrossPoint(x11, y11, x12, y12,	x21, y21, x22, y22)
		cv2.circle(MyClass._IMG_RGB_DSC, (int(cx)+x, int(cy)+y), 5, G.COLOR_RED, 2)
		
		#cv2.imshow('ea' + str(MyClass._INDEX), MyClass._IMG_RGB_DSC)
		# <<< GET MIDDLE POINT ----------


		topX, topY = int(sx)+x, int(sy)+y
		middleX, middleY = int(cx)+x, int(cy)+y
		bottomX, bottomY = int(ex)+x, int(ey)+y

		dst = MyClass._IMG_RGB_DSC[y-G.RESULT_MARGIN: y + h_ + G.RESULT_MARGIN*2, x-G.RESULT_MARGIN : x + w_+G.RESULT_MARGIN*2]

		return (MyClass._ERROR_CODE, dst,(topX, topY, middleX, middleY, bottomX, bottomY))

	def GetPointHB(data):
		#Return Format
		(dst,(topX, topY, middleX, middleY, bottomX, bottomY)) = (None,(0, 0, 0, 0, 0, 0))

		#주석을 하며 실행
		#return (MyClass._ERROR_CODE, dst,(topX, topY, middleX, middleY, bottomX, bottomY))

		# >>> ROI ----------
		(imgRoi, (x_, y_, w_, h_)) = ROI.GetUserROI(
			MyClass._IMG_SRC.copy(), MyClass._TYPE, MyClass._WEB, MyClass._INDEX)
		(x, y, w, h) = (x_, y_, w_, h_)


		#실 사용할 imgRoi, threshold
		(imgAutoRoi, sortListStats, (x_, y_, w_, h_), threshold) = ROI.GetAutoROI(
			imgRoi.copy(), MyClass._TYPE, x, y, w, h, MyClass._INDEX)


		# Component 합치기
		imgRgbRoi = cv2.cvtColor(imgRoi, cv2.COLOR_GRAY2BGR)

		arrID = None
		for i in range(2, len(sortListStats), 1):
			(x__, y__, w__, h__, _) = sortListStats[i]
			if abs(y_ - (y__+h__)) <= 5 and x__ >= x_:
				arrID = i
				break

		if arrID is not None:
			newContour = U.MergeContour(sortListStats[1], sortListStats[arrID])
			(x_, y_, w_, h_, _) = newContour

		(x_, y_, w_, h_, _) = (x_-10, y_-1, w_+20, h_+2, _) #보정
		(x, y, w, h) = (x+x_, y+y_, w_, h_)
		#cv2.rectangle(imgRgbRoi, (x_, y_), (x_+w_-1, y_+h_-1), G.COLOR_RED, 1)
		#cv2.imshow('hb' + str(MyClass._INDEX), imgRgbRoi)

		cv2.rectangle(MyClass._IMG_RGB_DSC, (x, y), (x+w-1, y+h-1), G.COLOR_GREEN, 1)
		#cv2.imshow('hb' + str(MyClass._INDEX), MyClass._IMG_RGB_DSC)


		# 사용하지 않음 [가로 라인 삭제]
		#(imgRoi, (x_, y_, w_, h_)) = ROI.SetFitROI(
		#	imgRoi.copy(), MyClass._TYPE, x, y, w, h, MyClass._INDEX)
		#(x, y, w, h) = (x+x_, y+y_, w_, h_)
		# <<< ROI ----------

		


		# >>> GET LINE ----------
		#TODO 우측라인 상하 분리 계산

		imgRoi = MyClass._IMG_SRC[y: y + h, x : x + w]
		imgRgbRoi = cv2.cvtColor(imgRoi, cv2.COLOR_GRAY2BGR)

		threshold1 = 300
		threshold2 = 900
		imgRoi = FC.GetCanny(imgRoi, MyClass._TYPE, threshold1, threshold2, MyClass._INDEX)

		length = int(float(MyClass._T1)/2)
		group = int(float(MyClass._T1)*2)
		lines = lineObj.GetLines(imgRoi, MyClass._TYPE, length, group, MyClass._INDEX)
		

		if lines is None:
			MyClass._ERROR_CODE = EM.MakeErrorCode(MyClass._TYPE, 4000)
			return (MyClass._ERROR_CODE, dst,(topX, topY, middleX, middleY, bottomX, bottomY))

		m = sys.maxsize
		listVerticalLines = []
		listHorizontalLines = []
		
		listPositiveLines = []
		listNegativeLines = []
		
		for line in lines:
			(x1, y1, x2, y2) = line[0]
			l = (x1, y1, x2, y2)

			if (y2==y1): #수평
				m=0
				listHorizontalLines.append(l)
				#cv2.line(imgRgbRoi, (int(x1), int(y1)), (int(x2), int(y2)), G.COLOR_BLUE, 1)

			elif (x2==x1): #수직
				listVerticalLines.append(l)
				#cv2.line(imgRgbRoi, (int(x1), int(y1)), (int(x2), int(y2)), G.COLOR_RED, 1)
			
			else:
				m = (y2-y1)/(x2-x1)

				if(abs(m)<=1): #사선
					if m>0:
						listPositiveLines.append(l)
					else:
						listNegativeLines.append(l)
					#cv2.line(imgRgbRoi, (int(x1), int(y1)), (int(x2), int(y2)), G.COLOR_BLUE, 1)

				else:	#오차가 심한 수직(제외)
					pass
					#listVerticalLines.append(l)
					#cv2.line(imgRgbRoi, (int(x1), int(y1)), (int(x2), int(y2)), G.COLOR_RED, 1)

		#수직 라인중 좌우 분리
		verticalLines = np.average(listVerticalLines, axis=0)
		(ax1, ay1, ax2, ay2) = verticalLines

		listLeftVLines = []
		listRightVLines = []
		for vl in listVerticalLines:
			(x1_, y1_, x2_, y2_) = vl
			l = (x1_, y1_, x2_, y2_)
			if(x1_<ax1):
				listLeftVLines.append(l)
			else:
				listRightVLines.append(l)

		#-----------------------------------------

		leftVLines = np.average(listLeftVLines, axis=0)
		(x1_, y1_, x2_, y2_) = leftVLines
		cv2.line(imgRgbRoi, (int(x1_), int(y1_)), (int(x2_), int(y2_)), G.COLOR_RED, 1)
		cv2.line(MyClass._IMG_RGB_DSC, (int(x1_)+x, int(y1_)+y), (int(x2_)+x, int(y2_)+y), G.COLOR_RED, 1)

		rightVLines = np.average(listRightVLines, axis=0)
		(x1_, y1_, x2_, y2_) = rightVLines
		cv2.line(imgRgbRoi, (int(x1_), int(y1_)), (int(x2_), int(y2_)), G.COLOR_RED, 1)
		cv2.line(MyClass._IMG_RGB_DSC, (int(x1_)+x, int(y1_)+y), (int(x2_)+x, int(y2_)+y), G.COLOR_RED, 1)

		pLines = np.average(listPositiveLines, axis=0)
		(x1_, y1_, x2_, y2_) = pLines
		cv2.line(imgRgbRoi, (int(x1_), int(y1_)), (int(x2_), int(y2_)), G.COLOR_RED, 1)
		cv2.line(MyClass._IMG_RGB_DSC, (int(x1_)+x, int(y1_)+y), (int(x2_)+x, int(y2_)+y), G.COLOR_RED, 1)

		nLines = np.average(listNegativeLines, axis=0)
		if len(listNegativeLines) != 0:
			(x1_, y1_, x2_, y2_) = nLines
			cv2.line(imgRgbRoi, (int(x1_), int(y1_)), (int(x2_), int(y2_)), G.COLOR_BLUE, 1)
			cv2.line(MyClass._IMG_RGB_DSC, (int(x1_)+x, int(y1_)+y), (int(x2_)+x, int(y2_)+y), G.COLOR_RED, 1)
		
		#cv2.imshow('hb' + str(MyClass._INDEX), imgRgbRoi)

		# <<< GET LINE ----------

		


		# >>> GET END POINT ----------
		(x11, y11, x12, y12) = rightVLines
		(x21, y21, x22, y22) = (0, 0, G.LINE_THICKNESS, 0) #top line
		(sx, sy) = U.GetCrossPoint(x11, y11, x12, y12,	x21, y21, x22, y22)
		cv2.circle(imgRgbRoi, (int(sx), int(sy)), 5, G.COLOR_RED, 2)
		topX, topY = int(sx)+x, int(sy)+y
		cv2.circle(MyClass._IMG_RGB_DSC, (int(sx)+x, int(sy)+y), 5, G.COLOR_RED, 2)



		(x21, y21, x22, y22) = (0, h_, G.LINE_THICKNESS, h_) #bottom line
		(ex, ey) = U.GetCrossPoint(x11, y11, x12, y12,	x21, y21, x22, y22)
		cv2.circle(imgRgbRoi, (int(ex), int(ey)), 5, G.COLOR_RED, 2)
		bottomX, bottomY = int(ex)+x, int(ey)+y
		cv2.circle(MyClass._IMG_RGB_DSC, (int(ex)+x, int(ey)+y), 5, G.COLOR_RED, 2)
		
		#cv2.imshow('hb' + str(MyClass._INDEX), imgRgbRoi)
		# <<< GET END POINT ----------



		# >>> GET MIDDLE POINT ----------

		if len(listNegativeLines) != 0:
			(x11, y11, x12, y12) = nLines
			(x21, y21, x22, y22) = rightVLines
			(sx, sy) = U.GetCrossPoint(x11, y11, x12, y12,	x21, y21, x22, y22)
			cv2.circle(imgRgbRoi, (int(sx), int(sy)), 5, G.COLOR_YELLOW, 2)
			cv2.circle(MyClass._IMG_RGB_DSC, (int(sx)+x, int(sy)+y), 5, G.COLOR_RED, 2)

		if len(listNegativeLines) != 0:
			(x11, y11, x12, y12) = nLines
			(x21, y21, x22, y22) = leftVLines
			(ex, ey) = U.GetCrossPoint(x11, y11, x12, y12,	x21, y21, x22, y22)
			cv2.circle(imgRgbRoi, (int(ex), int(ey)), 5, G.COLOR_YELLOW, 2)
			cv2.circle(MyClass._IMG_RGB_DSC, (int(ex)+x, int(ey)+y), 5, G.COLOR_RED, 2)
			my1 = ey
		else:
			#TODO 크로스 점 구할 수 없음 따라서 leftVLine y축 최소값으로 대치????
			my1 = 0



		(x11, y11, x12, y12) = pLines
		(x21, y21, x22, y22) = rightVLines
		(sx, sy) = U.GetCrossPoint(x11, y11, x12, y12,	x21, y21, x22, y22)
		cv2.circle(imgRgbRoi, (int(sx), int(sy)), 5, G.COLOR_YELLOW, 2)
		cv2.circle(MyClass._IMG_RGB_DSC, (int(sx)+x, int(sy)+y), 5, G.COLOR_RED, 2)

		(x11, y11, x12, y12) = pLines
		(x21, y21, x22, y22) = leftVLines
		(ex, ey) = U.GetCrossPoint(x11, y11, x12, y12,	x21, y21, x22, y22)
		cv2.circle(imgRgbRoi, (int(ex), int(ey)), 5, G.COLOR_YELLOW, 2)
		cv2.circle(MyClass._IMG_RGB_DSC, (int(ex)+x, int(ey)+y), 5, G.COLOR_RED, 2)
		my2 = ey



		mx = ex
		my = int(my2 - my1)/2 + my1
		cv2.circle(imgRgbRoi, (int(mx), int(my)), 5, G.COLOR_RED, 2)
		middleX, middleY = int(mx)+x, int(my)+y
		cv2.circle(MyClass._IMG_RGB_DSC, (int(mx)+x, int(my)+y), 5, G.COLOR_RED, 2)

		#cv2.imshow('hb' + str(MyClass._INDEX), imgRgbRoi)
		#cv2.imshow('hb' + str(MyClass._INDEX), MyClass._IMG_RGB_DSC)

		# <<< GET MIDDLE POINT ----------
		
		dst = MyClass._IMG_RGB_DSC[y-G.RESULT_MARGIN: y + h_ + G.RESULT_MARGIN*2, x-G.RESULT_MARGIN : x + w_+G.RESULT_MARGIN*2]

		return (MyClass._ERROR_CODE, dst,(topX, topY, middleX, middleY, bottomX, bottomY))

	def GetPointPI(data):
		#Return Format
		(dst,(topX, topY, middleX, middleY, bottomX, bottomY)) = (None,(0, 0, 0, 0, 0, 0))

		#주석을 하며 실행
		#return (MyClass._ERROR_CODE, dst,(topX, topY, middleX, middleY, bottomX, bottomY))
	
		# >>> ROI ----------
		(imgRoi, (x_, y_, w_, h_)) = ROI.GetUserROI(
			MyClass._IMG_SRC.copy(), MyClass._TYPE, MyClass._WEB, MyClass._INDEX)
		(x, y, w, h) = (x_, y_, w_, h_)
		#cv2.rectangle(MyClass._IMG_RGB_DSC, (x, y), (x+w-1, y+h-1), G.COLOR_RED, 1)
		#cv2.imshow('pi' + str(MyClass._INDEX), MyClass._IMG_RGB_DSC)
		

		#실 사용할 imgRoi, threshold
		(imgRoi, sortListStats, (x_, y_, w_, h_), threshold) = ROI.GetAutoROI(
			imgRoi.copy(), MyClass._TYPE, x, y, w, h, MyClass._INDEX)
		(x, y, w, h) = (x+x_, y+y_, w_, h_)
		#cv2.imshow('pi' + str(MyClass._INDEX), imgRoi)
		#cv2.rectangle(MyClass._IMG_RGB_DSC, (x, y), (x+w-1, y+h-1), G.COLOR_GREEN, 1)
		#cv2.imshow('pi' + str(MyClass._INDEX), MyClass._IMG_RGB_DSC)

		
		# 사용하지 않음 [가로 라인 삭제]
		#(imgRoi, (x_, y_, w_, h_)) = ROI.SetFitROI(
		#	imgRoi.copy(), MyClass._TYPE, x, y, w, h, MyClass._INDEX)
		#(x, y, w, h) = (x+x_, y+y_, w_, h_)
		# <<< ROI ----------


		# >>> GET END POINT ----------
		imgTopRoi = imgRoi[0: G.LINE_THICKNESS, 0 : w_]
		
		sortKey = G.COMPONENTS_SORT_KEY['area']
		(sortListStats) = compoObj.GetComponentStats(imgTopRoi, MyClass._TYPE, sortKey, MyClass._INDEX)
		(x__, y__, w__, h__, area__) = sortListStats[1]
		topX, topY = int(x__)+x, int(y__)+y
		cv2.circle(MyClass._IMG_RGB_DSC, (int(x__)+x, int(y__)+y), 5, G.COLOR_RED, 2)
		#cv2.imshow('pi' + str(MyClass._INDEX), MyClass._IMG_RGB_DSC)

		#------------------------------
		imgBottomRoi = imgRoi[h_-G.LINE_THICKNESS: h_, 0 : w_]

		(sortListStats) = compoObj.GetComponentStats(imgBottomRoi, MyClass._TYPE, sortKey, MyClass._INDEX)
		(x__, y__, w__, h__, area__) = sortListStats[1]
		bottomX, bottomY = int(x__)+x, int(h__)+h_-G.LINE_THICKNESS+y
		cv2.circle(MyClass._IMG_RGB_DSC, (int(x__)+x, int(h__)+h_-G.LINE_THICKNESS+y), 5, G.COLOR_RED, 2)
		#cv2.imshow('pi' + str(MyClass._INDEX), MyClass._IMG_RGB_DSC)

		# <<< GET END POINT ----------

		# >>> GET MIDDLE POINT ----------

		imgMiddleRoi = imgRoi[int(h_*1/4): h_- int(G.LINE_THICKNESS*3/4), w_-G.LINE_THICKNESS : w_]
		#imgMiddleRgbRoi = cv2.cvtColor(imgMiddleRoi, cv2.COLOR_GRAY2BGR)
		#cv2.imshow('pi' + str(MyClass._INDEX), imgMiddleRoi)
		
		(sortListStats) = compoObj.GetComponentStats(imgMiddleRoi, MyClass._TYPE, sortKey, MyClass._INDEX)
		(x__, y__, w__, h__, area__) = sortListStats[1]

		#cv2.rectangle(imgMiddleRgbRoi, (x__, y__), (x__+w__-1, y__+h__-1), G.COLOR_GREEN, 1)
		#cv2.circle(imgMiddleRgbRoi, (x__ + int(w__/2), y__ + int(h__/2)), 5, G.COLOR_RED, 2)
		#cv2.imshow('pi' + str(MyClass._INDEX), imgMiddleRgbRoi)

		cv2.rectangle(MyClass._IMG_RGB_DSC, (x__ + (w_-G.LINE_THICKNESS) + x, y__ + (int(h_*1/4)) + y),
			(x__+w__-1 + (w_-G.LINE_THICKNESS) + x, y__+h__-1 + (int(h_*1/4)) + y), G.COLOR_GREEN, 1)
		cv2.circle(MyClass._IMG_RGB_DSC, (x__ + int(w__/2) + (w_-G.LINE_THICKNESS) + x, y__ + int(h__/2) + (int(h_*1/4)) + y), 5, G.COLOR_RED, 2)
		#cv2.imshow('pi' + str(MyClass._INDEX), MyClass._IMG_RGB_DSC)

		# <<< GET MIDDLE POINT ----------

		middleX, middleY = x__ + int(w__/2) + (w_-G.LINE_THICKNESS) + x, y__ + int(h__/2) + (int(h_*1/4)) + y

		dst = MyClass._IMG_RGB_DSC[y-G.RESULT_MARGIN: y + h_ + G.RESULT_MARGIN*2, x-G.RESULT_MARGIN : x + w_+G.RESULT_MARGIN*2]

		return (MyClass._ERROR_CODE, dst,(topX, topY, middleX, middleY, bottomX, bottomY))
	
	def GetPointUA(data):
		#Return Format
		(dst,(topX, topY, middleX, middleY, bottomX, bottomY)) = (None,(0, 0, 0, 0, 0, 0))
		
		return MyClass.GetPointEA(data)

	# <<< Function ----------

	# >>> Class Variable ----------
	_INDEX = 0

	_IMG_SRC = None
	_IMG_RGB_DSC = None
	_W = 0
	_H = 0

	_TYPE = None
	_WEB = 0
	_FLANGE = 0
	_T1 = 0.0
	_T2 = 0.0

	_ERROR_CODE = None

	_FUNC = None

	_FUNCTIONS = {
		'ch': GetPointCH,
		'ea': GetPointEA,
		'hb': GetPointHB,
		'pi': GetPointPI,
		'ua': GetPointUA,
	}
	
	# <<< Class Variable ----------

	# __init__ : 클래스 인스턴스 생성시 초기화하며 실행되는 부분
	def __init__(self, type, index=None):
		# MyClass._TYPE = type.lower()
		MyClass._TYPE = type.lower()
		MyClass._INDEX = index
		MyClass._FUNC = MyClass._FUNCTIONS[type.lower()]



	def __str__(self):
		return f'str : {self._index}'
		# pass

	def __repr__(self):
		return f'str : {self._index}'
		# pass

	def __doc__(self):
		return f'str : {self._index}'
		# pass

	@classmethod
	def classMethod(self, arg):
		return None

	@staticmethod
	def staticMethod(self, arg):
		return None


	def Start(self, data, image):
		print('2')
		# dt = image.read()
		# encoded_img = np.fromstring(dt, dtype=np.uint8)
		# img = cv2.imdecode(encoded_img, cv2.IMREAD_GRAYSCALE)

		MyClass._IMG_SRC = image
		(MyClass._H, MyClass._W) = MyClass._IMG_SRC.shape[:2]

		MyClass._IMG_RGB_DSC = cv2.cvtColor(MyClass._IMG_SRC, cv2.COLOR_GRAY2BGR)
		# >>> GET PARSING DATA ----------
		(MyClass._WEB, MyClass._FLANGE, MyClass._T1, MyClass._T2) = U.GetParsingData(data, MyClass._INDEX)
		# return (MyClass._H, MyClass._W,(0, 0, 0, 0, 0, 0))
		print(MyClass._WEB, MyClass._FLANGE, MyClass._T1, MyClass._T2)

		# <<< GET PARSING DATA ----------
		return MyClass._FUNC(data)



