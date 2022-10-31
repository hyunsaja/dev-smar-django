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


# >>> user function >>>>>>>>>>>>>>>>>>>>

def GetStaticInfo(path, type):
	(_realW, _realT, _realA, _realB) = (0.0, 0.0, 0.0, 0.0)

	arr = path.split('-')

	(w, t) = arr[1:3]
	if w[0] == '0':
		w = w[1:]

	if t[0] == '0':
		t = t[1:]

	_realW = float(w)
	_realT = float(t)
	
	if type=='hb':
		(a, b) = arr[3:5]
		_realA = float(a)
		_realB = float(b)
		
	return (_realW, _realT, _realA, _realB)




def GetParsingData(data, index=None):
	(w, f, t1, t2) = (0.0, 0.0, 0.0, 0.0)

	data_ = data.strip().lower()
	# print(data_)
	(type_, spec_)= data_.split(' ')[0:2]
	print(type_, spec_)

	spec_ = spec_.replace('a', '')
	spec_ = spec_.replace('t', '')
	

	if type_ == 'ch':
		w, f, t = spec_.split('*')[0:3]
		t1, t2 = t.split('/')[0:2]
		#print(index, type_, w, f, t1, t2)
		t2= 0
		return (w, f, t1, t2)
		
	elif type_ == 'ea':
		w, f, t1 = spec_.split('*')[0:3]
		#print('======',index, type_, w, f, t1, t2)
		# print(w, f, t1, t2)
		return (w, f, t1, t2)

	elif type_ == 'hb':
		w, f, t = spec_.split('*')[0:3]
		t1, t2 = t.split('/')[0:2]
		#print('======', index, type_, w, f, t1, t2)
		return (w, f, t1, t2)

	elif type_ == 'pi':
		w, = spec_.split('-')[1:2]
		#print(index, type_, w, f, t1, t2)
		return (w, f, t1, t2)
		
	elif type_ == 'ua':
		w, f, t = spec_.split('*')[0:3]
		t1, t2 = t.split('/')[0:2]
		#print(index, type_, w, f, t1, t2)
		return (w, f, t1, t2)

	else:
		pass

	return (w, f, t1, t2)



# y-y1 = m(x-x1),	m=(y2-y1)/(x2-x1)
# y-y1 = 0,			y1==y2, m=0
# y = y1,			x1 = x2	
def GetCrossPoint(x11, y11, x12, y12,	x21, y21, x22, y22):
	(cx, cy) = (None, None)

	px= (x11*y12 - y11*x12)*(x21-x22) - (x11-x12)*(x21*y22 - y21*x22)
	py= (x11*y12 - y11*x12)*(y21-y22) - (y11-y12)*(x21*y22 - y21*x22)
	p = (x11-x12)*(y21-y22) - (y11-y12)*(x21-x22)

	if(p == 0):
		print('parallel')
		return (cx, cy) 


	cx = px/p
	cy = py/p
	return (cx, cy) 



def MergeContour(contr1, contr2):
	(contr) = None
	(x1, y1, w1, h1, _) = contr1
	(x2, y2, w2, h2, _) = contr2
	sx = x1 if x1 < x2 else x2
	sy = y1 if y1 < y2 else y2

	x1 = x1 + w1
	y1 = y1 + h1
	x2 = x2 + w2
	y2 = y2 + y2
	ex = x1 if x1 > x2 else x2
	ey = y1 if y1 > y2 else y2

	w = ex-sx
	h = ey-sy

	contr = [sx, sy, w, h, _]
	return contr

