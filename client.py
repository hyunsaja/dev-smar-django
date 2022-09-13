import requests
import json

headers = {'Content-type': 'application/json'}
      
url = 'http://127.0.0.1:8000/code_master/rpcag_speed_spec/'
# image = open('./image/img.bmp', 'rb')
# files = {'origin_image': image}
data = {
        'machineID' : '2',
        'machineKey' : 'smart-robot-007',
        'group_data' : 'S994~TG7',
        'view_data' : 'S994~TG7~01~EA01',
        'inputlength' : '9300',
        'standard' : 'EA 65*65*6T',
        'texture' : 'SS400',
        'project': '8138',
        'por': 'L40',
        'seq': '3',
        }
# flask host로 보낼때 
# msg = requests.post(url, headers=headers, data=json.dumps(data), timeout = 50).text

# smart-robot.kr 로 보낼때
msg = requests.post(url, headers=headers, data=json.dumps(data), timeout = 50).text
print(msg)