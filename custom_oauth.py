import requests
import json
import logger

with open("configuration.json","r") as json_file:
    configuration = json.load(json_file)





def get_refresh_token():

    params = {
        "code": configuration["Zoho"]["Code"],
        "grant_type": "authorization_code",
        "client_id": configuration["Zoho"]["Client ID"],
        "client_secret": configuration["Zoho"]["Client secret"],
        "redirect_uri": "https://www.zoho.com"
    }

    #request for the refresh token
    resp = requests.post(url = "https://accounts.zoho.com/oauth/v2/token",
                         params=params)
    
    resp_content_as_json = json.loads(resp.content)
    logger.log("custom_oauth.py | Request is sent to the zoho for getting refresh token. Response is: " + str(resp_content_as_json))

    if("error" in resp_content_as_json):
        logger.log("custom_oauth.py | something went wrong during requesting refresh token, probably token is expired or used before")
    else:
        return resp_content_as_json["refresh_token"]






def refresh(refresh_token):
    params = {
        "refresh_token":refresh_token,
        "client_id": configuration["Zoho"]["Client ID"],
        "client_secret": configuration["Zoho"]["Client secret"],
        "scope": configuration["Zoho"]["Scope"],
        "redirect_uri": "https://www.zoho.com",
        "grant_type": "refresh_token"
    }

    resp = requests.post(url = "https://accounts.zoho.com/oauth/v2/token",
                         params=params)
    

    resp_content_as_json = json.loads(resp.content)
    

    

    if("error" in resp_content_as_json):
        logger.log("custom_oauth.py | something went wrong during requesting refresh token, probably token is expired or used before")
    else:
        access_token = resp_content_as_json["access_token"]
    
        logger.log("custom_oauth.py | access token is returned")
        return(access_token)

    



