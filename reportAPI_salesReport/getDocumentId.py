import requests
import json
import os


host = "https://sellingpartnerapi-na.amazon.com/reports/2021-06-30/reports/"

# get access token from file "accessToken.json"
acc = r""

with open(acc, "r", encoding="utf-8") as file:
    access = json.load(file)

token = access["access_token"]

# Create Header 
header = {

"Accept-Encoding" : "gzip, deflate, br"
,"Connection" : "keep-alive"
,"Accept" : "application/json"
,"x-amz-access-token" : token

}


# get reportId

reportId_path = r"reportId.json"

with open(reportId_path, "r", encoding= "utf-8") as file2:
        accessID = json.load(file2)

reportID = accessID["reportId"]


# get documentId

url = f"{host}{reportID}"

response = requests.get(url, headers = header)
response_json = response.json()
documentId = response_json['reportDocumentId']
status = response_json["processingStatus"]


# save documentId.json
output_path = os.path.join(os.path.dirname(__file__), "documentId.json")
with open(output_path, "w" , encoding= "utf-8") as f:
        json.dump(response_json, f, ensure_ascii=False, indent=4)

print(response)
print(response_json)
print(f"Document ID: {documentId}")
print(f"Status: {status}")
