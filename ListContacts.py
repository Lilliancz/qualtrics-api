
# [START gae_python37_app]
from flask import Flask


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')

import requests
import json
import pandas as pd
import csv

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
final.to_csv('rest.csv')


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
