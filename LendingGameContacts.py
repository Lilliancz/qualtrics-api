# This file downloads a contact list from the Qualtrics research core
# It splits the embedded data dictionary into separate columns
# It also removes columns (see line 50)
# If you need to preserve those columns that have been dropped, just delete them from the list
# The column list also includes more columns than you might have since it is specific to 
# the lending game contact list. Just remove those that don't match your list.

import requests
import json
import pandas as pd
import csv
import os
import time

# this version accepts manual input from the user
apiToken = input("Enter your API token: ")
mailingListID = input("Enter your Mailing List ID, e.g., ML_XXXXXXXXXX:")
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

# reads csv, but all values are loaded as string.
df = pd.read_csv('contacts.csv')

# convert embedded data to dict using apply(eval)
# to check type, use .apply(type)
ed = df.embeddedData.apply(eval)
df2 = ed.apply(pd.Series)

# concatenate old with new
final = pd.concat([df, df2], axis=1)

# drop junk
final = final.drop(
    columns=["id", "firstName", "embeddedData", "lastName", "email", "language", "unsubscribed", "responseHistory",
             "emailHistory", "A_Info", "B_Info", "C_Info", "D_Info", "E_Info", "F_Info", "G_Info", "H_Info", "I_Info",
             "J_Info", "DateTaken", "TriggerResponseID", "TriggerSurveyID"])

# save to csv
timestr = time.strftime("%Y%m%d-%H%M%S")
final.to_csv('lendingGameData'+timestr+".csv")
os.remove("contacts.csv")
