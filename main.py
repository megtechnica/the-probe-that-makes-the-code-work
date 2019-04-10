from pylink import *
from pycampbellcr1000 import *
from asyncio import *
from datetime import *
import os
import convert_logger_data

def main():
    ## capture device logic here
    device = CR1000.from_url()
    data = device.get_data('Data_Logger_Output', start_time)
    init_rec_nm = data['RecNm']
    while device.connected == True:
        
        


def get_seconds():
    time_stamp = datetime.now()
    return time_stamp.second

def get_seconds_CR1000():
    time_stamp = device.gettime()
    return time_stamp.second


def ten_second_interval(ts_1):
    ts_2 = datetime.now()
    time_delta = ts_2.second - ts_1.second
    if time_delta >= abs(10):
        return True
    else:
        return False

## Upon powering on the Raspberry Pi and the CR1000X
## this will run.
start_time = datetime.now()
wait_for = 10 - start_time.second
try:
    main()

except NoDeviceException:
    ## ct is Crash Time
    ## cts is Crash Time Stamp
    cts = datetime.now()
    ct = "{0}:{1}:{2}".format(cts.hour, cts.minute, cts.second)
    crash_log = open("crashlog.txt","w+")
    crash_log.write("\nConnection to device failed at {0}".format(ct))
    crash_log.close()
    os.system('sudo shutdown -r now')
