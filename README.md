# Connectivity-with-no-auth
Python app for SAP Cloud foundry to read data from On-premise system

The App is capable of reading on-premise data using the SAP Cloud connector and Connectivity services of Cloud foundry (SAP) .
More information about this APP and background can be found on the blog below :

https://blogs.sap.com/2019/09/23/exposing-on-premise-data-to-sap-cloud-foundry/

The APP has below mentioned files :

runtime.txt - Has the information regarding the runtime 
requirements.txt - Information regarding the libraries which needs to be installed when the app is deployed to the CF env
read_data.py - Main file with python code to read the data from Onpremise system
Procflie - code to execute the python script on deployment 
manifest.yml - bind services of CF to the APP
