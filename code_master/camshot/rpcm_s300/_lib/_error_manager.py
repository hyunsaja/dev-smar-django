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



#[call style]
#MyClass._ERROR_CODE = EM.MakeErrorCode(MyClass._TYPE, 9000)

_ERROR_CODE={
    0: '',
    1: '',

    #입력 파라메타
    1000: '입력 파라메타',
    1001: '입력 값이 None',
    1002: '입력 값이 너무 작음',
    1003: '입력 값이 너무 큼음',
    1004: '입력 값이 음수',
    1005: 'OOOOOOOOOOOOOOOO',
    1006: 'OOOOOOOOOOOOOOOO',


    #리턴 format 에러
    2000: '리턴 format 에러',

    #변수
    3000: '변수',

    #배열, 리스트 등
    4000: '배열, 리스트 등',

    #이미지 포맷
    5000: '이미지 포맷',

    #이미지 크기
    6000: '이미지 크기',

    #TEST
    9000: 'TEST',
    9001: 'TEST1',
    9002: 'TEST2',
}



def MakeErrorCode(type, code, index=None):
    errorCode= {
		'type': type,
		'code' : code,
        'description' : None,
		'call_stack': None
	}

    errorCode['description'] = _ERROR_CODE[code]

    call_stack= ''
    currentFrame = inspect.currentframe()
    callFrame = inspect.getouterframes(currentFrame, 2)
    for callF in callFrame:
        call_stack = call_stack + (str(callF[0]) + '\r\n')

    errorCode['call_stack'] = call_stack

    return errorCode





