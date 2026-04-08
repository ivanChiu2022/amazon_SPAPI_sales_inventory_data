# Amazon SP-API Report Automation


This project automates the process of generating **Sales**, **Inventory** reports from Amazon Selling Partner API (SP-API) using Python scripts and a batch file.


# Folder Structure

AVC/

├── accessToken/
        accessToken.json # Stores access token after generation
        data.json # Contains credentials required to request access token
        getAccessToken.py # Python script to generate access token


├── reportAPI_invReport/
        documentId.json # Stores document ID response for inventory report
        reportId.json # Stores Report ID for inv report
        getDocumentId.py # Gets document ID using report ID
        getReportId.py # Submits report request to get report ID
        getReportURL.py # Downloads report from URL using document ID


├── reportAPI_salesReport/
        documentId.json # Stores document ID response for Sales report
        reportId.json # Stores Report ID for Sales report
        getDocumentId.py # Gets document ID using report ID
        getReportId.py # Submits report request to get report ID
        getReportURL.py # Downloads report from URL using document ID


├── generateAllReports.bat # Main batch file to run all steps

Report generation step (# just double click the bat file "processing_sales_Inv_nppm_Report.bat" under AVC folder)
below is how the program run step by step


# processing


1) Generate Access Token 

1.1 prepare the necessary from amazon AVC as below
and save it as a json file under folder \AVC\accessToken  file name "data.json"

        {
    "Content-Type" : "application/x-www-form-urlencoded;charset=UTF-8"
    ,"client_id" : "amzn1.application-XXXXXXXXX" 
    ,"client_secret" : "amzn1.oa2-XXXXXXXX" 
    ,"grant_type" : "refresh_token"
    ,"refresh_token" : "Atzr|XXXXXXXXXXXXXXXXXXXXXXXXXXXXX" 
} 
    
1.2 run python file getAccessToken.py
1.3 AccessToken will be stored in file name "accessToken.json" under \AVC\accessToken

2) Generate report ID for forecast, Sales, Inventory and nppm report. 

2.1 report data
Official report name : 
    - GET_VENDOR_SALES_REPORT

        Report Option : 

        "reportPeriod": "WEEK", # Generate the report last week (From Sunday to Sat )
        "distributorView": "SOURCING",
        "sellingProgram": "RETAIL"
        "dataEndTime" : last Sat
        "dataStartTime" : pervious Sun
        "marketplaceIds": ["ATVPDKIKX0DER"] # North America

    - GET_VENDOR_INVENTORY_REPORT
        
        Report Option : 

        "reportPeriod": "WEEK", # Generate the report last week (From Sunday to Sat )
        "distributorView": "SOURCING",
        "sellingProgram": "RETAIL"
        "dataEndTime" : last Sat
        "dataStartTime" : pervious Sun
        "marketplaceIds": ["ATVPDKIKX0DER"] # North America
        
    - GET_VENDOR_NET_PURE_PRODUCT_MARGIN_REPORT
    
        Report Option : 

        "reportPeriod": "WEEK", # Generate the report last week (From Sunday to Sat )
        "dataEndTime" : last Sat
        "dataStartTime" : pervious Sun
        "marketplaceIds": ["ATVPDKIKX0DER"] # North America
        
    - GET_VENDOR_TRAFFIC_REPORT

        Report Option : 

        "reportPeriod": "WEEK", # Generate the report last week (From Sunday to Sat )
        "sellingProgram": "RETAIL"
        "dataEndTime" : last Sat
        "dataStartTime" : pervious Sun
        "marketplaceIds": ["ATVPDKIKX0DER"] # North America

    - GET_VENDOR_FORECASTING_REPORT
        
        Report Option : 

        "reportPeriod": "WEEK", # Generate the report last week (From Sunday to Sat )
        "sellingProgram": "RETAIL"
        "marketplaceIds": ["ATVPDKIKX0DER"] # North America
        


2.2 excute 3 python files "getReportId.py under below folders 
    - \AVC\reportAPI_salesReport
    - \AVC\reportAPI_invReport
    - \AVC\reportAPI_nppmReport
    - \AVC\reportAPI_trafficReport
    - \AVC\reportAPI_forecastReport

    the reportid.json will be stored in those folders 


3) Cooldown Period

after report IDs ready , keep in mind that Amazon needs about 1 mins (60 sec) to generate the report
the bat file already included the 60 sec cooldown period to wait amazon to generated the report after reportIDs stored. 

4) GET Document IDs

after 60 Sec cooldown period completed , the application will be send request to amazon to generate the DocumentId , and store the docmuentId.json in each folder. 

if the reprot status = DONE, thats mean we can generate the report immediately 

if report status is Queny , thats mean amazon needs more time to generate the report # need to consider if 60 sec cool down period is not enough. 

if the report status is FATAL , thats mean there are some issue in the report we want to generate , may be the data is not ready. 

5) Report URL and report convertion

5.1 once the report ready , we can use the document ID stored in file documentId.json to get the report downlaod link. 
the report will auto download in gzin format, that gzip file fille be stored in the new created foldeer , the folder name should be {TODAY} + {REPORTNAME}

5.2 the gzip file will be un-zip as json file and stored in same folder and saved as same file name with the folder. 

5.3 if the data is correct , the application will convert the json file to csv file in the same folder. 

# How to generate the report 
as per mention : just double click the .bat file "generateAllReports.bat" in \AVC
please keep in mind again 

Amazon recommends waiting 48–72 hours after the end of the reporting week.
Run the report on Tuesday for the previous week's data.


