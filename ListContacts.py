import requests
import json
import io, os
import sys
import pandas
from pandas.io.json import json_normalize
 
 
apiToken = 'MYAPITOKEN'
mailingListID = "ML_XXXXXXXXXXXXXX"
fileFormat = "csv"
dataCenter = 'umich'
 
baseUrl = "https://{0}.qualtrics.com/API/v3/mailinglists/{1}/contacts/".format(dataCenter, mailingListID)
headers = {
    "content-type": "application/json",
    "x-api-token": apiToken,
    } 

requestDownloadUrl = baseUrl
requestDownload = requests.request("GET", requestDownloadUrl, headers=headers, stream=True)
 

data = json.loads(requestDownload.content)
data = requestDownload.content
df = pandas.read_csv(io.StringIO(data.decode("utf-8")))
print(df)	
