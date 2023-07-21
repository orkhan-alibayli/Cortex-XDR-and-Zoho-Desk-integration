import requests
import json
import custom_oauth
import logger


#Read the configuration file
with open("configuration.json","r") as json_file:
    configuration = json.load(json_file)


refresh_token = None
if(refresh_token == None):
    refresh_token = custom_oauth.get_refresh_token()


access_token = custom_oauth.refresh(refresh_token)

headers = {
        "Authorization":"Zoho-oauthtoken " + access_token,
        "Content-Type":"application/json"
}



def initiate_variables(index):


    variables = {
        "zoho_contact_id": configuration["Tenants"][index]["Zoho Contact ID"],
        "tenant_name" : configuration["Tenants"][index]["Tenant Name"],
        "contact_number": configuration["Tenants"][index]["Contact Number"],
        "contact_email": configuration["Tenants"][index]["Contact Email"],
        "zoho_department_id": configuration["Tenants"][index]["Zoho Department ID"],
    }


    return variables

def send_request(parsed_incident_fields, variables):
    global headers

    custom_fields = {
        "cf_incident_severity": parsed_incident_fields["severity"],
        "cf_incident_id_1": parsed_incident_fields["incident_id"],
        "cf_incident_date_and_time": parsed_incident_fields["creation_time"]
    }

    body = {
        "entitySkills" : [ "18921000000379001", "18921000000364001", "18921000000379055", "18921000000379031" ],
        "subCategory" : "Sub General",
        "productId" : "",
        "contactId" : variables["zoho_contact_id"],
        "subject" : "MDR - " + variables["tenant_name"] + " -" + " Incident ID: " + parsed_incident_fields["incident_id"],
        "dueDate" : "2016-06-21T16:16:16.000Z",
        "departmentId" : variables["zoho_department_id"],
        "channel" : "SmartIT SOC - Service Desk", 
        "description" : parsed_incident_fields["description"],
        "language" : "English",
        "priority" : "NotDefined",
        "classification" : "",
        "phone" : variables["contact_number"],
        "category" : "cortex xdr",
        "email" : variables["contact_email"], # this is the customer mail
        "status" : "Open",
        "cf" : custom_fields
        }
    
    
    res = requests.post(url="https://desk.zoho.com/api/v1/tickets",
                        headers=headers, json=body)
    
    resp_content_as_json = json.loads(res.content)

    logger.log("zoho.py | Request is sent to the zoho")


    #access token expires after 1 hour. if it is expired we are getting error. if there is an error the token should be refreshed
    if("errorCode" in resp_content_as_json):
        logger.log("zoho.py | The token is probably expired: " + str(resp_content_as_json))
        if(resp_content_as_json["errorCode"] == "INVALID_OAUTH"):
            new_access_token = custom_oauth.refresh(refresh_token)

            headers = {
            "Authorization":"Zoho-oauthtoken " + new_access_token,
            "Content-Type":"application/json"
        }
            logger.log("zoho.py | Access token is refreshed")
            
        send_request(parsed_incident_fields, variables)
    else:
        return
