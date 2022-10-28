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

def GetContours(imgSrc, type, index=None):
	(sortListContours, hier)  = ([], None)

	(contours, hier) = cv2.findContours(imgSrc, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	listContours = []
	if(contours is not None):
		for contr in contours:

			area = cv2.contourArea(contr)
			contrInfo = (area, contr)
			listContours.append(contrInfo)

		sortListContours = sorted(listContours, key=lambda row: (row[0]), reverse=True)

	return (sortListContours, hier)


