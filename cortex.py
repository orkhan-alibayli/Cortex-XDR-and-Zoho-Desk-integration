import requests
import json
import time
import time_converter
import zoho
from datetime import datetime
import logger


#Read the configuration file
with open("configuration.json","r") as json_file:
    configuration = json.load(json_file)



def initiate_variables(index):

    api_key = configuration["Tenants"][index]["API key"]
    api_key_id = configuration["Tenants"][index]["API key id"]

    variables = {
        "url": configuration["Tenants"][index]["Tenant URL"] + "/public_api/v1/incidents/get_incidents",
        "headers": {
            "x-xdr-auth-id": str(api_key_id),
            "Authorization": api_key
        }
    }

    return variables



#makes api call to get incident data and returns the data
def send_request(body, variables):
    
    res = requests.post(url=variables["url"],
                        headers=variables["headers"],
                        json=body)

    return res



def parse_incident_fields(index_of_incident, incident_fields):

    incident_id = incident_fields["reply"]["incidents"][index_of_incident]["incident_id"]
    severity = incident_fields["reply"]["incidents"][index_of_incident]["severity"]
    description = incident_fields["reply"]["incidents"][index_of_incident]["description"]
    url_to_incident = incident_fields["reply"]["incidents"][index_of_incident]["xdr_url"]
    creation_time = time_converter.convert_time(incident_fields["reply"]["incidents"][0]["creation_time"])

    incident_description = "<b>" + "New incident has been created!" + "</b>" + "<br />" + "<br />" + "<b>" + "Incident description: " + "</b>" + description + "<br />" + "<br />" + "<b>" + "Incident ID: " "</b>" + incident_id + "<br />" + "<br />" + "<b>" + "Url to incident: " + "</b>" + url_to_incident + "<br />"

    parsed_incident_fields = {"severity":severity, "description":incident_description, "incident_id":incident_id, "creation_time":creation_time}

    return parsed_incident_fields



def call_zoho(index):

    while(True):
        time.sleep(60)

        epoch_time=int(time.time() - 60) * 1000

        body = {
            "request_data":{
                "filters": [
                    {
                        "field":"creation_time",
                        "value":epoch_time,
                        "operator": "gte"
                    }
                ]
            }
        }


        variables = initiate_variables(index)

        res = send_request(body, variables)
        incident_fields = json.loads(res.content)

        #for debugging purposes
        logger.log("cortex.py " + "[ " + str(index) + " ]" + "| response of API call to cortex xdr: " + str(res.content))

        if(incident_fields["reply"]["total_count"] !=0):

            incident_count = incident_fields["reply"]["total_count"]
            index_of_incident = 0

            while (index_of_incident < incident_count):



                parsed_incident_fields = parse_incident_fields(index_of_incident, incident_fields)


                variables = zoho.initiate_variables(index)
                zoho.send_request(parsed_incident_fields, variables)

                index_of_incident = index_of_incident + 1