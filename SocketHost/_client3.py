import requests
import json

headers = {'Content-type': 'application/json'}
      
url = 'http://smart-robot.kr/code_master/rpcm_camshot/'
image = open('./30000.bmp', 'rb')
files = {'image': image}
data = {
        'machineID' : '3',
        'machineKey' : 'smart-robot-007',
        'group_data' : 'S994~TG7',
        'view_data' : '9999-999-99-B99-999-1',
        'inputlength' : '4100',
        'standard' : '65*16T',
        'texture' : 'SS400',
        'project': '8138',
        'por': 'L40',
        'seq': '3',
        'm_data': 'aaaa,9790,dafa,dfa'
        }
# flask host로 보낼때 
# msg = requests.post(url, headers=headers, data=json.dumps(data), timeout = 50).text

# django 로 보낼때
msg = requests.post(url, files=files, data=data, timeout= 50).text
print(msg)