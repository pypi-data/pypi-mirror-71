import queue
import datetime
import time
from datetime import datetime
import threading
import requests
import json
from flask import request,g
from rfc3339 import rfc3339


buffer = queue.Queue()
flag = False

with open('config.json') as json_data_file:
    config = json.load(json_data_file)
buffer_size = int(config['buffer_size'])
timeout = int(config['timer'])
API_ENDPOINT = config['END_POINT']
END_POINT_TO_SIMULATE_DB=config['END_POINT_TO_SIMULATE_DB']
time_to_refresh_cofg_file = int(config['time_to_refresh_cofg_file'])
#fetching first time data from simulating_db api
response = requests.get(END_POINT_TO_SIMULATE_DB)
response=response.json()
includes = response[0]
levels=response[1]

def load_config_file():
    global includes
    global levels
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print('LOADING CONFIG FILE', current_time)
    response = requests.get(END_POINT_TO_SIMULATE_DB)
    response=response.json()
    includes = response[0]
    levels=response[1]
    Timer.cancel()
    start_timer()

Timer=threading.Timer(time_to_refresh_cofg_file,load_config_file) 
    
def start_timer():
    print('inside timer')
    Timer=threading.Timer(time_to_refresh_cofg_file,load_config_file) 
    Timer.start()


count = 0


def hit_the_api():
    global buffer
    global count
    global API_ENDPOINT
    print('SENDING DATA TO DATABASE AT TIME ',
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    data = (list(buffer.queue))
    buffer.queue.clear()
    print(data)
    r = requests.post(url=API_ENDPOINT, json=data)
    count=0 



def get_request_body(request):
    if (request.get_json() is not None):
        posted_data = request.get_json()    
    elif (request.form != {}):
        posted_data = request.form
    elif (request.content_type == 'text/plain'):
        posted_data = request.data
    else:
        posted_data=None
    return posted_data    
    
    
t = threading.Timer(timeout, hit_the_api)

def main_logic_for_sending_logs(message):
    list = {}
    list['message'] = (message)
    global count
    global t
    global buffer
    count = count + 1
    if count == 1:
        t = threading.Timer(timeout, hit_the_api)
        t.start()
    if(buffer.qsize()>=buffer_size-1):
        buffer.put(list)
        t.cancel()
        hit_the_api()    
    else:
        buffer.put(list)


def sendLog(message):
    global flag
    global includes
    global levels
    print('inside send log method')

    if flag == False:
            flag = True
            start_timer()  

    if isinstance(message,dict):
        level = message['level']
        if (len(levels) == 1 and levels[0] == '*'):
            main_logic_for_sending_logs(message)
        elif (level in levels):
            main_logic_for_sending_logs(message)
    else:     
        #filtering logic
        print(includes, len(includes))
        print(levels, len(levels))
        if (len(includes) == 1 and includes[0] == '*'):
            main_logic_for_sending_logs(message)
        elif(request.path  in includes):
            main_logic_for_sending_logs(message)


def info(message):
    level = 'INFO'
    list = {}
    list['timestamp']=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    list['level']=level
    list['data']=message
    print(list)
    sendLog(list)
def error(message):
    level = 'ERROR'
    list = {}
    list['timestamp']=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    list['level']=level
    list['data']=message
    sendLog(list)
def warn(message):
    level = 'WARN'
    list = {}
    list['timestamp']=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    list['level']=level
    list['data']=message
    sendLog(list)




def log_request(response):
    print('after every request')
    now = time.time()
    duration = round(now - g.start, 2)
    dt = datetime.fromtimestamp(now)
    timestamp = rfc3339(dt, utc=True)

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    host = request.host.split(':', 1)[0]
    args = dict(request.args)

    log_params = [
        ('method', request.method),
        ('path', request.path),
        ('status', response.status_code),
        ('duration', duration),
        ('time', timestamp),
        ('ip', ip),
        ('host', host),
        ('params', args)
    ]

    request_id = request.headers.get('X-Request-ID')
    if request_id:
        log_params.append(('request_id', request_id))

    log_params.append(('request_body', get_request_body(request)))
    headers=[]
    for h in response.headers:
        headers.append(h)
    log_params.append(('resonse_headers',headers))
    log_params.append(('response_body', response.data.decode("utf-8")))
    print(json.dumps(log_params))
    print(type(json.dumps(log_params)))
    sendLog(json.dumps(log_params))
    return response
    