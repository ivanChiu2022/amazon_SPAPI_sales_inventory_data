
import requests
import json
from datetime import datetime, timedelta, timezone
import os


# API HOST
host = "https://sellingpartnerapi-na.amazon.com/reports/2021-06-30/reports"

# get access token from file "accessToken.json"
acc = r"your access token file here"

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


#Get report date

# find last saturday
def get_last_saturday():
    today = datetime.today()
    offset = (today.weekday() - 5) % 7  # Saturday is weekday 5
    last_saturday = today - timedelta(days=offset)
    return last_saturday.date()

lastSat = get_last_saturday()

# find the first sunday before saturday 

def get_first_sunday_before_last_saturday():
    today = datetime.today()
    
    # Find last Saturday
    offset_to_saturday = (today.weekday() - 5) % 7
    last_saturday = today - timedelta(days=offset_to_saturday)

    # Find the Sunday before that Saturday (6 days earlier)
    sunday_before = last_saturday - timedelta(days=6)
    
    return sunday_before.date()

wkBegan = get_first_sunday_before_last_saturday()


# for special period
dateBack_end = 3 # for non SAT ending period , data will available after period end 3 days

dateBack_start = dateBack_end + 1 # change the no of days to define the report period.

# calculate the start date and end date for special period. 

endDay = datetime.now(timezone.utc) - timedelta(days = dateBack_end)
startDay = datetime.now(timezone.utc) - timedelta(days = dateBack_start)

# copy and replace the wkBegan and lastSat value in the dataStartTime and dataEndTime variances

#print(lastSat)
#print(wkBegan)








# isoformat function 
def iso8601(d) :
    return d.strftime('%Y-%m-%dT00:00:00Z') #iso8601 format , amazon request

# format the targetdate
dataStartTime = iso8601(wkBegan)
dataEndTime = iso8601(lastSat)

#  

# Create Body 

payload  = {
  "reportType": "GET_VENDOR_NET_PURE_PRODUCT_MARGIN_REPORT",
  "marketplaceIds": ["ATVPDKIKX0DER"],
  "reportOptions":{"reportPeriod": "WEEK"},
  "dataStartTime" : dataStartTime,
  "dataEndTime" : dataEndTime,

}


# made request (Create Report and Get Report ID)

response = requests.post(host, headers=header, json=payload)
response_json = response.json()
reportId = response_json.get("reportId")

# save reportId.json
output_path = os.path.join(os.path.dirname(__file__), "reportId.json")
with open(output_path, "w", encoding = "utf-8") as f:
    json.dump(response_json, f, ensure_ascii=False, indent=4)




#handle response 

print(f"Report : {payload['reportType']}")

print(f"Start Date: {dataStartTime}")
print(f"End Date: {dataEndTime}")

print("Status Code: ",response.status_code)
print("reportID:", reportId)
print(f"Saved reportId to {output_path}")




