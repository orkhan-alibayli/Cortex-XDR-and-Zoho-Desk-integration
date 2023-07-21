from time import strftime, localtime
from pytz import timezone,utc
from datetime import datetime


def convert_time(epoch_time):

    incident_time = datetime.utcfromtimestamp(epoch_time/1000).strftime('%Y-%m-%d %H:%M:%S')
    
    return incident_time