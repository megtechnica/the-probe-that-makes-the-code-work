from pylink import *
from pycampbellcr1000 import *
from asyncio import *
from datetime import *
import os
import convert_logger_data

def main():
    start_time = datetime.now()
    ## capture device logic here
    device = CR1000()
    while device.connected == True:
        




def ten_second_interval(ts_1, ts_2):
    time_delta = ts_2.second - ts_1.second
    if time_delta >= abs(10):
        return True
    else:
        return False



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
