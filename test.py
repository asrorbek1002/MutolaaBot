# while True:
#     print("""  
#     ___     ___   
#   /  __ \ / __  \    
#  / /    \ /    \ \   
# | |   I love   | |   
#  \ \  coding   / /   
#   \ \         / /     
#    \ \       / /     
#     \ \     / /      
#      \ \   / /      
#       \ \ / /        
#        \   /     
#         \ /   
#           """)


import requests
import json

# Define the inputBody and headers
input_body = {
    "tasks": {
        "import-1": {
            "operation": "import/webpage",
            "url": "https://api.freeconvert.com/v1/process/jobs/6658b98f828c08e90995353b"
        },
        "convert-1": {
            "operation": "convert",
            "input": "import-1",
            "input_format": "webpage",
            "output_format": "jpg",
            "options": {
                "margin": "0",
                "hide_cookie": True,
                "use_print_stylesheet": True
            }
        },
        "export-1": {
            "operation": "export/url",
            "input": [
                "convert-1"
            ]
        }
    }
} 

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer {access-token}'
}

url = "https://api.freeconvert.com/v1/process/jobs"

# Make a POST request and print the response
response = requests.post(url, data=json.dumps(input_body), headers=headers)

if response.status_code == 200:
    response_json = response.json()
    print(response_json)
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)
