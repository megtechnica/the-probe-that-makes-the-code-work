from pylink, pycampbellcr1000, asyncio, datetime import *
import os, convert_logger_data

## I like your haircut

## declaring functions, not the entry point
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

async def data_capture(device, count_index_nm):
    data = device.get_data('Data_Logger_Output', start_time)
    return capt_data = data[count_index_nm]

def main():
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
    ## RecNbr = 391
    count_index_nm = 0
    ## while device is connected
    while device.connected == True:
        ts_1 = get_seconds_CR1000()
        capt_data = await data_capture(device, count_index_nm)
        conv_data = asyncio.create_task(convert_data(capt_data))
        await conv_data





## Upon powering on the Raspberry Pi and the CR1000X
## this will run.  The initial data capture does not 
## occur immediately, therefore we need to wait 10 sec
## for the first capture.  

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
