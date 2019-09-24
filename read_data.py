from flask import Flask , render_template 
from cfenv import AppEnv
import os
import requests
import base64
import json

#create an app using flask lib and also get the port info for later use
app = Flask(__name__)
app.config["DEBUG"] = True
cf_port = os.getenv("PORT")
######################################################################
############### Step 1: Read the environment variables ###############
######################################################################
env = AppEnv()
#read all the xsuaa service key values from the env variables
uaa_service = env.get_service(name='xsuaa-demo')
#read all the connectivity service key values from the env variables
conn_service = env.get_service(name='connectivity-demo-lite')
# read the client ID and secret for the connectivity service
conn_sUaaCredentials = conn_service.credentials["clientid"] + ':' + conn_service.credentials["clientsecret"]
# read the On premise proxy host and on premise proxy port for the connectivity service
proxy_url = conn_service.credentials["onpremise_proxy_host"] + ':' + conn_service.credentials["onpremise_proxy_port"]
######################################################################
##### Step 2: Request a JWT token to access the connectivity service##
######################################################################
#create authorization with basic authentication using connectivity credentials as base64 format
headers = {'Authorization': 'Basic '+ base64.b64encode(bytes(conn_sUaaCredentials ,'utf-8')).decode(), 'content-type': 'application/x-www-form-urlencoded'}
#create formdata with client ID and grant type
formdata = [('client_id', conn_service.credentials["clientid"] ), ('grant_type', 'client_credentials')]
#call the xsuaa service to retrieve JWT
response_conn = requests.post(uaa_service.credentials["url"] + '/oauth/token', data=formdata, headers=headers)
#convert the response to a proper format which can be reused again
jwt_conn = response_conn.json()["access_token"]
######################################################################
##### Step 3: Make a call to backend system via SAP CC to read data ##
######################################################################
#Set up basic auth for SAP System - Username and Password
onpremise_auth = requests.auth.HTTPBasicAuth('<enter your SAP Username of the on-premise system>' , '<Enter the password>!')
#Enter the exact path to your OData service in the SAP System using the virtual host:port details mentioned in the SAP Cloud Connector
url_cc =  'http://vhost.atosorigin-ica.com:8080/sap/opu/odata/sap/Z_TRANSPORTS_CDS/Z_TRANSPORTS?$format=json'
#create a dict with proxy relevant information
proxyDict = { 'http' : proxy_url }
#create a header with authorization to the proxy server with the JWT retrieved in Step 2
headers = {
'content-type': 'application/json',
'Proxy-Authorization': 'Bearer ' + jwt_conn,
'cache-control': 'no-cache'
}
#make a get request using the Virtual ODATA url using the proxy details , header and basic authorization for Onpremise system
response = requests.get( url_cc, proxies=proxyDict, headers=headers, auth = onpremise_auth)
#conver the data 
data_response = json.loads(response.text)
######################################################################
##### Step 4: Return the data and run the app                       ##
######################################################################
@app.route('/')
def index():
  return data_response

if __name__ == '__main__':
	if cf_port is None:
		app.run(host='0.0.0.0', port=5000, debug=True)
	else:
		app.run(host='0.0.0.0', port=int(cf_port), debug=True)
