import os
import shutil
import cv2
import numpy as np
# from matplotlib import pyplot as plt



def imgshot(image, height):   
    
    try:
        # steel = cv2.imread('./image/' + filename + '.bmp', cv2.IMREAD_GRAYSCALE)    
        # steel = cv2.imread("./image/steel2.bmp")   
        # height, width, channel = steel.shape
        # steel2 = cv2.getRotationMatrix2D((width/2, height/2), 25, 1)
        # steel3 = cv2.warpAffine(steel, steel2, (width, height))
        steel4 = image[63:1038, 490:1465].copy()  #[상, 하, 좌, 우] 조명영역
        # steel4 = steel[122:1055, 639:1580].copy()  #full bed 영역

        # src = steel3[500:1000, 100:1430].copy()   
        src = steel4.copy()
        src2 = steel4.copy()
        


        # img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
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

        f = open("./cam/file/point.txt", "w")


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
                    
                    
                    cv2.drawContours(src2, cnt2, -1,(255 ,0,255), 2)

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
        f.close()
        
        shutil.copy('./cam/file/point.txt', './cam/file/nc.cnc')  # 서버환경 
        dst = cv2.resize(img, dsize=(480, 360), interpolation=cv2.INTER_AREA)
        cv2.imwrite('./cam/image/img.jpg', dst)
        # msg는 finally 파트에서 ruturn
        msg = 'ShotOK'
    
    except:
        msg='ImageError'
    
    finally:
        return msg