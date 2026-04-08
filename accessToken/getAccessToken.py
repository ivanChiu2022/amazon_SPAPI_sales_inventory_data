import requests
import json


host = "https://api.amazon.com/auth/o2/token"



# data.json cannot be share to others

with open("data.json", "r") as file: 
    data = json.load(file)


headers = {
    "Accept-Encoding" : "gzip, deflate, br"
    ,"Connection" : "keep-alive"
    ,"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
}



# made request
response = requests.post(host, headers=headers, data=data)


# get the access Token
if response.status_code == 200:
    token_data = response.json()
    print("Access Token:", token_data["access_token"])

# save the accessToken to accessToken.json
    with open("accessToken.json", "w") as json_file:
        json.dump(token_data, json_file, indent=4)

    print("token saved to accessToken.json")

#Error Handling
else:
    print("Error:", response.status_code)
    print("Response: ", response.text)

