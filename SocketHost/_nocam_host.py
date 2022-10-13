import sys
import openpyxl
import json
import os
import os.path
import time
import math
import requests
import sqlite3 as s
import numpy as np
import cv2
import socket, threading
import _camshot
import _imgshot

def imgshot1(src):    
    try:
        #src = cv2.imread('./image/' + '10' + '.bmp', cv2.IMREAD_GRAYSCALE)
        # ROI  ---------------------------------------------------------------------------------------
        # src.shape : 1080(h), 1920(w)
        x=810; y=350; w=300; h=380
        roi = src[y:y+h, x:x+w]  
        #cv2.imshow('roi',roi)
        pos = 70
        #  이진화 -------------------------------------------------------------------------------------        
        #roi = cv2.adaptiveThreshold(roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 5)
        #_, roi = cv2.threshold(roi, pos, 255, cv2.THRESH_BINARY) #반전:cv2.THRESH_BINARY_INV,자동:cv2.THRESH_OTSU
        #roi = cv2.GaussianBlur(roi, (0, 0), 1.0)
        cv2.imwrite('./images/'+'00'+'.jpg', roi)
        #  find edge ------------------------------------------------------------------------------- 
        # kernel = np.ones((3,3),np.uint8)                # dilate -> erode : 닫기 연산
        # roi = cv2.dilate(roi,kernel,iterations = 1) # 팽창 
        # cv2.imwrite('./images/'+'01'+'.jpg', roi)
        # kernel = np.ones((3,3),np.uint8)
        # roi = cv2.erode(roi,kernel,iterations = 1) # 침식
        # cv2.imwrite('./images/'+'02'+'.jpg', roi)
        roi = cv2.Canny(roi,30,100,apertureSize = 3,L2gradient=False)
        cv2.imwrite('./images/'+'03'+'.jpg', roi)
        kernel = np.ones((5,5),np.uint8)                # dilate -> erode : 닫기 연산
        roi = cv2.dilate(roi,kernel,iterations = 1) # 팽창 
        cv2.imwrite('./images/'+'04'+'.jpg', roi)
        kernel = np.ones((3,3),np.uint8)
        roi = cv2.erode(roi,kernel,iterations = 1) # 침식
        cv2.imwrite('./images/'+'05'+'.jpg', roi)
        kernel = np.ones((3,3),np.uint8)
        roi = cv2.erode(roi,kernel,iterations = 1) # 침식
        cv2.imwrite('./images/'+'06'+'.jpg', roi)

        
        minLen = 150
        maxGap = 5
        lines = cv2.HoughLinesP(roi, 1, np.pi/180, 150, minLineLength= minLen , maxLineGap= maxGap)
        print(lines)
        img = cv2.cvtColor(roi,cv2.COLOR_GRAY2BGR)
        for i in range(len(lines)):
            for x1,y1,x2,y2 in lines[i]:
                cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
        print(range(len(lines)))
        cv2.imwrite('./images/'+'07'+'.jpg', img)

        '''
        ret, corners = cv2.findChessboardCorners(roi, (9,6),None)
        img2 = cv2.cvtColor(roi,cv2.COLOR_GRAY2BGR)
        cv2.drawChessboardCorners(img2, (9,6), corners,ret)
        cv2.imwrite('./images/'+'07'+'.jpg', img2)
        '''
        # 결과 이미지 출력 -----------------------------------------------------------------------------    
        #cv2.imshow('img', img)
        msg = 'shoot OK >>>>>'
        return msg
    except:
        print('형식 오류')
        msg='Error,'
        client_socket.sendall(msg.encode())         
        cv2.destroyAllWindows()   
        return
    finally:
        pass

def camshot1(src):    
    try:
        #src = cv2.imread('./image/' + '10' + '.bmp', cv2.IMREAD_GRAYSCALE)
        # ROI  ---------------------------------------------------------------------------------------
        x=700; y=312; w=230; h=400  
        roi = src[y:y+h, x:x+w]  
        #cv2.imshow('roi',roi)
        cv2.imwrite('./image/'+'00'+'.jpg', roi)
        #  find edge -------------------------------------------------------------------------------        
        filter = True
        #roi = cv2.GaussianBlur(roi, (0, 0), 1.0)
        edges = cv2.Canny(roi,50,100,apertureSize = 3,L2gradient=True)
        cv2.imwrite('./image/'+'01'+'.jpg', edges)
        kernel = np.ones((3,3),np.uint8)                # dilate -> erode : 닫기 연산
        edges = cv2.dilate(edges,kernel,iterations = 1) # 팽창 
        cv2.imwrite('./image/'+'02'+'.jpg', edges)
        kernel = np.ones((5,5),np.uint8)
        edges = cv2.erode(edges,kernel,iterations = 1) # 침식
        #cv2.imshow('canny',edges)
        cv2.imwrite('./image/'+'03'+'.jpg', edges)
        lines = cv2.HoughLines(edges,1,np.pi/180,150)
        if not lines.any():
            print('No lines were found')
            msg = 'No line >>>>>'
            return msg
        if filter:
            rho_threshold = 15
            theta_threshold = 0.1

            # how many lines are similar to a given one
            similar_lines = {i : [] for i in range(len(lines))}
            for i in range(len(lines)):
                for j in range(len(lines)):
                    if i == j:
                        continue
                    rho_i,theta_i = lines[i][0]
                    rho_j,theta_j = lines[j][0]
                    if abs(rho_i - rho_j) < rho_threshold and abs(theta_i - theta_j) < theta_threshold:
                        similar_lines[i].append(j)

            # ordering the INDECES of the lines by how many are similar to them
            indices = [i for i in range(len(lines))]
            indices.sort(key=lambda x : len(similar_lines[x]))

            line_flags = len(lines)*[True]
            for i in range(len(lines) - 1):
                if not line_flags[indices[i]]: 
                    continue
                for j in range(i + 1, len(lines)):
                    if not line_flags[indices[j]]: 
                        continue
                    rho_i,theta_i = lines[indices[i]][0]
                    rho_j,theta_j = lines[indices[j]][0]
                    if abs(rho_i - rho_j) < rho_threshold and abs(theta_i - theta_j) < theta_threshold:
                        line_flags[indices[j]] = False 

        print('number of Hough lines:', len(lines))

        filtered_lines = []
        if filter:
            for i in range(len(lines)): # filtering
                if line_flags[i]:
                    filtered_lines.append(lines[i])

            print('Number of filtered lines:', len(filtered_lines))
        else:
            filtered_lines = lines
        img = cv2.cvtColor(src,cv2.COLOR_GRAY2BGR)
        for line in filtered_lines:
            rho,theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 300*(-b))+700        
            y1 = int(y0 + 300*(a))+312
            x2 = int(x0 - 300*(-b))+700
            y2 = int(y0 - 300*(a))+312
            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
            #print(x1,y1,x2,y2)
        cv2.imwrite('./image/'+'04'+'.jpg', img)
        
        # 결과 이미지 출력 -----------------------------------------------------------------------------    
        #cv2.imshow('img', img)
        msg = 'shoot OK >>>>>'
        return msg
    except:
        print('형식 오류')
        msg='Error,'
        client_socket.sendall(msg.encode())         
        cv2.destroyAllWindows()   
        return
    finally:
        #client_socket.close()
        pass


def temp(): 
    try:
        print('Connected by', addr)
        recvdata = client_socket.recv(1024)
        recvstr = recvdata.decode('utf-8').split(',')
        print(recvstr)
        cmd = recvstr[0]
        print(cmd)
        
        if 'camshot' in cmd:
            msg = _camshot.camshot(recvdata)
            client_socket.sendall(msg.encode()) 
            
        elif 'imgshot' in cmd:
            msg = _imgshot.imgshot() 
            res = msg.decode('utf-8').split(',')
            if 'ingshotOK' in res:
                return msg  
            else:
                return 'imgshotError'   
                     
        else:
            return 'keyError'
    except:
        return 'exceptError'
        
    
if __name__ == '__main__':   
    while True:
        time.sleep(0.05)
        HOST = '127.0.0.1'
        PORT = 9999
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        while True:
            try:
                print('listen...')
                client_socket, addr = server_socket.accept()
                th = threading.Thread(target=temp(), args = (client_socket,addr))
                th.start()
                #th.join()
            except:
                pass
