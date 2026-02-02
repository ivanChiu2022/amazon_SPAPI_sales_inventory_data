: get Access Token

cd accessToken
python getAccessToken.py

echo accessTokenDone

cd ..

:: Get reports ID 
:: get sales report ID

cd reportAPI_salesReport
python getReportId.py

echo Sales ReportID Done



::get Inv Report ID 

cd ..
cd reportAPI_invReport
python getReportId.py

echo Inv ReportID Done




::  waits for 60 seconds (1 minutes) for report generation.

timeout /t 60 

::Doc IDs and Generate reports
::Get INV Document ID
python getDocumentId.py 

echo Inv DocumentID Done

:: Generate Inv Report 

python getReportURL.py

echo INV Report Done

:: Get Sales Document ID

cd ..
cd reportAPI_salesReport
python getDocumentId.py 

echo Sales DocumentID Done
:: Generate Inv Report 

python getReportURL.py

echo Sales Report Done






pause