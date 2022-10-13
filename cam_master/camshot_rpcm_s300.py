import json
import time
import numpy as np
import cv2
from .models import PlateChamferMachine, RpcmS300Machine, RpcmAgcutMachine
from .models import CoamingMachine, MijuRobotWeldingMachine
from PIL import Image



def camshot(userid, machineid):
    try:
        data = CamMaster.objects.filter(UserID=userid, MachineID=machineid).last()
        image = data.origin_image.path
        src = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        # ROI  ---------------------------------------------------------------------------------------
        x = 800
        y = 400
        w = 300
        h = 200
        roi = src[y:y + h, x:x + w]
        cv2.rectangle(roi, (0, 0), (h - 1, w - 1), (0, 255, 0))

        #  find edge -------------------------------------------------------------------------------
        filter = True
        # roi = cv2.GaussianBlur(roi, (0, 0), 1.0)
        edges = cv2.Canny(src, 50, 100, apertureSize=3, L2gradient=True)
        kernel = np.ones((3, 3), np.uint8)  # dilate -> erode : 닫기 연산
        edges = cv2.dilate(edges, kernel, iterations=1)  # 팽창
        kernel = np.ones((5, 5), np.uint8)
        edges = cv2.erode(edges, kernel, iterations=1)  # 침식
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 150)

        if not lines.any():
            msg = 'No line >>>>>'
            return msg
        if filter:
            rho_threshold = 15
            theta_threshold = 0.1

            # how many lines are similar to a given one
            similar_lines = {i: [] for i in range(len(lines))}
            for i in range(len(lines)):
                for j in range(len(lines)):
                    if i == j:
                        continue
                    rho_i, theta_i = lines[i][0]
                    rho_j, theta_j = lines[j][0]
                    if abs(rho_i - rho_j) < rho_threshold and abs(theta_i - theta_j) < theta_threshold:
                        similar_lines[i].append(j)

            # ordering the INDECES of the lines by how many are similar to them
            indices = [i for i in range(len(lines))]
            indices.sort(key=lambda x: len(similar_lines[x]))

            line_flags = len(lines) * [True]
            for i in range(len(lines) - 1):
                if not line_flags[indices[i]]:
                    continue
                for j in range(i + 1, len(lines)):
                    if not line_flags[indices[j]]:
                        continue
                    rho_i, theta_i = lines[indices[i]][0]
                    rho_j, theta_j = lines[indices[j]][0]
                    if abs(rho_i - rho_j) < rho_threshold and abs(theta_i - theta_j) < theta_threshold:
                        line_flags[indices[j]] = False

                        # print('number of Hough lines:', len(lines))

        filtered_lines = []
        if filter:
            for i in range(len(lines)):  # filtering
                if line_flags[i]:
                    filtered_lines.append(lines[i])

            # print('Number of filtered lines:', len(filtered_lines))
        else:
            filtered_lines = lines
        image = cv2.cvtColor(src, cv2.COLOR_GRAY2BGR)
        for line in filtered_lines:
            rho, theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 300 * (-b)) + 700
            y1 = int(y0 + 300 * (a)) + 312
            x2 = int(x0 - 300 * (-b)) + 700
            y2 = int(y0 - 300 * (a)) + 312
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
            # print(x1,y1,x2,y2)
        data.result_image = image
        data.save()
        msg = 'shoot OK >>>>>'
        return msg
    except:
        return ({'massage': 'cam_Error'})