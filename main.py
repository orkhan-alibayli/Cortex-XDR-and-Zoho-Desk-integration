import cortex
import json
import logger
import threading


with open("configuration.json","r") as json_file:
    configuration = json.load(json_file)


#finding tenant counts
i = 0
while(True):

    if(str(i) in configuration["Tenants"]):
        i = i + 1
    else:
        break

max_index = i - 1
logger.log("main.py | found " + str(max_index +1) + " tenants")



for index in range(0, max_index + 1):

    #cortex.call_zoho(index)

    thrd = threading.Thread(target=cortex.call_zoho, args=(str(index),))
    thrd.start()