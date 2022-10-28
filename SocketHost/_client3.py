import requests
import json

headers = {'Content-type': 'application/json'}
      
# url = 'http://smart-robot.kr/code_master/rpcm_camshot/'
url = 'http://127.0.0.1:8000/code_master/rpcm_camshot/'
image = open('./image/CH.bmp', 'rb')
files = {'image': image}
data = {
        'machineID' : '3',
        'machineKey' : 'smart-robot-007',
        # EA 50*50*4T, UA 125*75*7/7T, CH 100*50*6/8.5T,
        # IB 150*125*8.5/14T, HB 125*125*6.5/9T, PI 103A-114.3, SP 75*75
        #'m_data': '"camshot","HB 125*125*6.5/9T", "878", "50.5", "1385", "0", "0", "0", "45", "45", "0", "0"',
        'm_data': 'camshot,EA 50*50*4T,878,50.5,1385,0,0,0,0,0,0,0,0',
        'cam_name':'aaaa'
        }
# flask host로 보낼때 
# msg = requests.post(url, headers=headers, data=json.dumps(data), timeout = 50).text

# django 로 보낼때
msg = requests.post(url, files=files, data=data, timeout= 50).text
print(msg)