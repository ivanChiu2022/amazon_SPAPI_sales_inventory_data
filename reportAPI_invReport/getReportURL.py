import requests
import json
import os
import gzip
import shutil
from datetime import datetime
import pandas as pd

host =  "https://sellingpartnerapi-na.amazon.com/reports/2021-06-30/documents/"

# get access Token

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


# get report ID

documentId_Path = r"C:\Users\XXXX\XXXX\documentId.json"

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
report_name = f"{today_str}_AVC_INV_REPORT"


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


# Helper functions for safe extraction
def get_amount(d):
    return d.get("amount") if isinstance(d, dict) else None

def get_currency(d):
    return d.get("currencyCode") if isinstance(d, dict) else None

# convert json file to csv 

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# extract inv data list
invData = data.get("inventoryByAsin", [])

# Flatten records with safe access for nested cost fields


# Flatten the structure
flattened = []
for item in invData:
    flattened.append({
        "startDate": item.get("startDate"),
        "endDate": item.get("endDate"),
        "ASIN": item.get("asin"),
        "sourceableProductOutOfStockRate": item.get("sourceableProductOutOfStockRate"),
        "procurableProductOutOfStockRate": item.get("procurableProductOutOfStockRate"),
        "Open Purchase Order Quantity": item.get("openPurchaseOrderUnits"),
        "receiveFillRate": item.get("receiveFillRate"),
        "Overall Vendor Lead Time (days)": item.get("averageVendorLeadTimeDays"),
        "sellThroughRate": item.get("sellThroughRate"),
        "unfilledCustomerOrderedUnits": item.get("unfilledCustomerOrderedUnits"),
        "Vendor Confirmation Rate": item.get("vendorConfirmationRate"),

        "Net Received Units": item.get("netReceivedInventoryUnits"),

        "Sellable On Hand Units": item.get("sellableOnHandInventoryUnits"),

        "Unsellable On Hand Units": item.get("unsellableOnHandInventoryUnits"),

        "Aged 90+ Days Sellable Units": item.get("aged90PlusDaysSellableInventoryUnits"),

        "unhealthyInventoryUnits": item.get("unhealthyInventoryUnits")
    })
# Convert to DataFrame and export to csv
df = pd.DataFrame(flattened)
df.to_csv(csv_path, index=False)

print(f"✅ CSV file saved as: {csv_path}")
