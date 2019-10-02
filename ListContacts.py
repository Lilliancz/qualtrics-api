# This version only creates the CSV of contacts but doesn't split up the embedded data. That's next on the list. pandas!!

import requests
import json
import pandas as pd
import csv

 
 
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

data = json.loads(requestDownload.content)['result']['elements']

# there is no header row in the csv, so the header names are just taken from the keys in the first row of the data
with open('contacts.csv', 'w', encoding='utf8', newline='') as output_file:
    mylist = csv.DictWriter(output_file,
                            fieldnames=data[0].keys(),
                            )
    mylist.writeheader()
    mylist.writerows(data)

df = pd.read_csv('contacts.csv')
ed = df.embeddedData.apply(eval)
df2 = ed.apply(pd.Series)
final = pd.concat([df, df2], axis=1)
final.to_csv('rest.csv')