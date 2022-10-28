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


IS_DEBUG = True

IS_DEBUG_GetBilateral = IS_DEBUG and False
IS_DEBUG_GetThreshold = IS_DEBUG and False
IS_DEBUG_GetCANNY = IS_DEBUG and False
IS_DEBUG_GetLines = IS_DEBUG and False




COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (255, 0, 0)
COLOR_RED = (0, 0, 255)
COLOR_YELLOW= (0, 255, 255)
COLOR_AQUA= (255, 255, 0)
COLOR_FUCHSIA= (255, 0, 255)
COLOR_WHITE = (255, 255, 255)

#PIX2MM = 0.2645833333
PIX2MM = {
    'ch': 0.4,
    'ea': 0.3,
    'hb': 0.3,
    'pi': 0.3,
}

LINE_THICKNESS = 6

ROI_X_BASE = {
    'ch': 455,
    'ea': 430,
    'hb': 410,
    'pi': 430,
}
ROI_Y_BASE ={
    'ch': 790,
    'ea': 770,
    'hb': 850,
    'pi': 800,
} 

ROI_WIDTH = 300
ROI_HEIGHT = 0


# >>> 임계값 설정하는 곳 --------------------
# first core value
THRESHOLD_RATE = {
    'ch': 2.5,
    'ea': 2.5,
    'hb': 2.7,
    'pi': 2.7,
}

CONTOUR_AREA = {
    'ch': 500,
    'ea': 1000,
    'hb': 1000,
    'pi': 1000,
}

# <<< 임계값 설정하는 곳 --------------------


COMPONENTS_SORT_KEY = {
    'x': 0,
    'y': 1,
    'w': 2,
    'h': 3,
    'area': 4,
}

COMPONENTS_AREA_REMOVE = {
    'ch': 100,
    'ea': 100,
    'hb': 50,
    'pi': 100,
}

#저장 이미지 여백
RESULT_MARGIN = 20