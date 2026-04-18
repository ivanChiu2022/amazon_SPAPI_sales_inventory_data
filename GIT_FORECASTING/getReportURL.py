import requests
import json
import os
import gzip
import shutil
from datetime import datetime
import pandas as pd

host =  "https://sellingpartnerapi-na.amazon.com/reports/2021-06-30/documents/"

# get access Token

acc = r"your access token file"

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


# get report ID

documentId_Path = r"documentId.json"

with open(documentId_Path, "r", encoding= "utf-8") as file3: 
    docId = json.load(file3)

documentId = docId['reportDocumentId']

url = f"{host}{documentId}"

response = requests.get(url=url, headers=header)
response_json = response.json()
reportURL = response_json['url']
filetype = response_json['compressionAlgorithm']



download_header = {

    "Accept" : "application/json"
    ,"x-amz-access-token" : token

}

#report Name YYYYMMDD(today)_AVC_SALES_REPORT
today_str = datetime.now().strftime("%Y%m%d")
report_name = f"{today_str}_GET_VENDOR_FORECASTING_REPORT"


# create report path and folder
base_dir = os.path.dirname(__file__)
report_folder = os.path.join(base_dir, report_name)
os.makedirs(report_folder, exist_ok=True)

gzip_path = os.path.join(report_folder, f"{report_name}.gz")
json_path = os.path.join(report_folder, f"{report_name}.json")
csv_path = os.path.join(report_folder, f"{report_name}.csv")

# download report


with requests.get(reportURL,  stream=True) as r:
    if r.status_code == 200: 
        with open(gzip_path, "wb") as f: 
            shutil.copyfileobj(r.raw, f)
        print(f"GZIP file saved as: {gzip_path}")

    else:
        print(f"fail to download, status_code : {r.status_code}")
        print(r.text)
        exit()

# un-zip the gzip file to json file

with gzip.open(gzip_path, 'rb') as f_in:
    with open(json_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
print(f"✅ Extracted JSON file saved as: {json_path}")

# convert json file to csv 

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Access the salesByAsin array
fc_data = data.get("forecastByAsin", [])

# Flatten nested fields
flattened = []
for item in fc_data:
    flattened.append({
        "startDate": item.get("startDate"),
        "endDate": item.get("endDate"),
        "asin": item.get("asin"),
        "forecastGenerationDate": item.get("forecastGenerationDate"),
        "MEAN": item.get("meanForecastUnits"),
        "P70": item.get("p70ForecastUnits"),
        "P80": item.get("p80ForecastUnits"),
        "P90": item.get("p90ForecastUnits")
    })

# Convert to DataFrame and save
if flattened:
    df = pd.DataFrame(flattened)
    df.to_csv(csv_path, index=False)
    print(f"✅ Converted to CSV: {csv_path}")
else:
    print("❌ No data found in salesByAsin.")












