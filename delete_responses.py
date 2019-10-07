import requests

//manually enter these
apiToken = ''
surveyId = ""
responseID = ""
dataCenter = 'umich'

url = "https://{0}.qualtrics.com/API/v3/surveys/{1}/responses/{2}".format(dataCenter, surveyId, responseID)
headers = {
    'accept': 'application/json',
    "x-api-token": apiToken
}
querystring = {"decrementQuotas":"false"}

response = requests.request("DELETE", url, headers=headers, params=querystring)

print(response.text)
