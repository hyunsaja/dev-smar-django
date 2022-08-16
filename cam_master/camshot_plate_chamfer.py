import numpy as np
import cv2
from .models import CamMaster
from django.core.files import File
from django.core.files.base import ContentFile

def camshot(UserID, MachineID):
    try:
        height = 15
        data = CamMaster.objects.filter(UserID=UserID, MachineID=MachineID).last()
        # db에서 이미지 읽어올때 path로 읽어옴
        src_image = data.origin_image.path
        image = cv2.imread(src_image, cv2.IMREAD_GRAYSCALE)
        # 목대 작업 ---------------------------------------------------------------
        src = image[63:1038, 490:1465].copy()  #[상, 하, 좌, 우] 조명영역

        ret, img_binary = cv2.threshold(src, 250, 255, 0)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        dst = cv2.morphologyEx(img_binary, cv2.MORPH_CLOSE, kernel, iterations=3)

        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        dst2 = cv2.morphologyEx(dst, cv2.MORPH_OPEN, kernel2, iterations=3)
        img = cv2.bitwise_not(dst2)
        contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)


        for cnt in contours:
            cv2.drawContours(src, [cnt], 0, (0, 0, 0),-1)

        # img2_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

        ret, img2_binary = cv2.threshold(src, 50, 255, 0)
        img_real = cv2.bitwise_not(img2_binary)
        img_real = cv2.bitwise_not(img_real)

        dist = cv2.distanceTransform(img_real, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)
        ring = cv2.inRange(dist, 11.5, 12.5)

        contours2, hierarchy = cv2.findContours(ring, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        with open("point.txt", mode="w", encoding="utf-8") as f:

            f.write("N0000 G90\n")
            lineNo = 2

            for cnt2 in contours2:

                for idx2, point in enumerate(cnt2):
                    x = float(point[0][0])*((((720-height)*2.4)/4)/975)*0.898
                    y = float(point[0][1])*((((720-height)*2.4)/4)/975)*0.8838
                    roundx = round(-x+134.45, 3)
                    roundy = round(y+303.075, 3)

                    if 900 < len(cnt2) < 1000:
                        # print(len(cnt2))
                        # print(idx2)


                        cv2.drawContours(src, cnt2, -1,(255 ,0,255), 2)

                        if idx2 == 0:
                            startx = round(roundx - 10, 3)
                            starty = round(roundy - 10, 3)
                            f.write("N0001 G00 X{} Y{} F10\n".format(startx,starty))
                            f.write("N0002 G01 X{} Y{} F10\n".format(roundx,roundy))

                        else:
                            lineNo = lineNo + 1
                            num = format(lineNo, '04')
                            f.write("N{} G01 X{} Y{} F10\n".format(num,roundx,roundy))

                        if len(cnt2)-1 == idx2:
                            lineNo = lineNo + 1
                            num = format(lineNo, '04')
                            lastx = round(roundx - 10, 3)
                            lasty = round(roundy - 10, 3)
                            f.write("N{} G00 X{} Y{}\n".format(num,lastx,lasty))

        nc = open('point.txt')
        data.ncfile.save('nc.cnc', File(nc), save=False)
        dst = cv2.resize(img, dsize=(480, 360), interpolation=cv2.INTER_AREA)
        ret, buf = cv2.imencode('.jpg', dst)  # dst: cv2 / np array
        content = ContentFile(buf.tobytes())
        data.result_image.save('img.jpg', content, save=False)
        data.sim_point = {'1': '2'}
        data.save()
        msg = 'ShotOK'
        return msg

    except:
        msg='Plate_Chamfer_Camshot_Error'