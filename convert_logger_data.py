from asyncio import *

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