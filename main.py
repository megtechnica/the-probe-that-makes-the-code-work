from pylink import *
from pycampbellcr1000 import *
from asyncio import *
from datetime import *
import os

## I like your haircut

## declaring functions, not the entry point
def convert_pressure(mV):
    return (((mV/5) + 0.095)/0.009)

def convert_relative_humidity(mV):
    return ((mV - 0.826)/0.0315)

def convert_farenheit(mV):
    return (((mV/0.01)*1.8)+32)

async def convert_data(data):
    for i in data:
        if "P" in i:
            data[i] = convert_pressure(data)
        elif "Therm" in i:
            data[i] = convert_farenheit(data)
        elif "Humid" in i:
            data[i] = convert_relative_humidity(data)
        else:
            continue
    return data

def get_seconds():
    time_stamp = datetime.now()
    return time_stamp.second

def get_seconds_CR1000():
    time_stamp = device.gettime()
    return time_stamp.second

def ten_second_interval(ts_1):
    ts_2 = datetime.now()
    return ts_2.second - ts_1

async def data_capture(device, count_index_nm):
    data = device.get_data('Data_Logger_Output', start_time)
    return capt_data = data[count_index_nm]

async def main():
    ## captures starting timestamp
    start_time = datetime.now()
    ## capture device logic here
    directory = listdir('/dev')
    if 'ttyACM0' in directory:
        device = CR1000.from_url('serial:/dev/ttyACM0:115200')
    else:
        device = CR1000.from_url('serial:/dev/ttyACM1:115200')
    ## once we connect to the device, capture a second time stamp & add that 
    ## to the start_time.second then subtract that from 10.  Sleep for 10 - runtime
    ## until this point.
    after_capture = get_seconds_CR1000()
    wait_for = 10 - (start_time.second + after_capture)
    sleep(wait_for)

    ## first data row capture happens here
    data = device.get_data('Data_Logger_Output', start_time)
    ## captures first record number to reference all other captures from
    init_rec_nm = data[0]['RecNbr']
    count_index_nm = 0
    ## while device is connected
    while device.connected == True:
        ## gets time stamp from the start of each loop
        ts_1 = get_seconds_CR1000()
        ## captures data from logger & awaits it
        capt_data = loop.create_task(data_capture(device, count_index_nm))
        await asyncio.wait(capt_data)
        await asyncio.sleep(0)
        ## passes capt_data into convert_data
        conv_data = loop.create_task(convert_data(capt_data))
        await asyncio.wait(capt_data)
        count_index_nm +=1
        time_delta = ten_second_interval(ts_1)
        await asyncio.sleep(time_delta)
        





## Upon powering on the Raspberry Pi and the CR1000X
## this will run.  The initial data capture does not 
## occur immediately, therefore we need to wait 10 sec
## for the first capture.  

loop = asyncio.get_event_loop()
task = loop.create_task(main)

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

except NoDeviceException:
    ## ct is Crash Time
    ## cts is Crash Time Stamp
    cts = datetime.now()
    ct = "{0}:{1}:{2}".format(cts.hour, cts.minute, cts.second)
    crash_log = open("crashlog.txt","w+")
    crash_log.write("\nConnection to device failed at {0}".format(ct))
    crash_log.close()
    os.system('sudo shutdown -r now')

finally:
    loop.close()
