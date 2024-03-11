import json
import requests
import base64

username = "ffilippi"
password = "ParkSlope03!"

# Encode the username and password in base64
credentials = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")

url = 'https://elk-kibana.shared-tst.tanonprod.aegon.io/internal/search/ese'
headers = {
    "kbn-xsrf": "true",  # This header is required for all mutating operations.
    "Authorization": f"Basic {credentials}",
    "Content-Type": "application/json"
}


data = {
    "params": {
                "index": "ff",

        "body": {
            "query": {
    "bool": {

      "filter": [
        {
          "match_phrase": {
            "application-id": "test-shared-aws-advisor-partners-app-svc"
          }
        }
      ],
    }},
            "size": 1000  # Number of rows (documents) to return
        }
    }
}
 
print ("Before Posting")
response = requests.post(url, headers=headers, data=json.dumps(data))
print("After Posting")
if response.status_code == 200:
    print("Json")
    results = response.json()
    print(results)
    for hit in results['rawResponse']['hits']['hits']:
        print(hit['_source'])  # Print each row (document)
else:
    print(f"Request failed with status code {response.status_code}")


