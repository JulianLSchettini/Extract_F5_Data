import requests
from requests.auth import HTTPBasicAuth

# Link and credentials to the JSON
url = "https://X.X.X.X/mgmt/tm/ltm/pool"
username = "your_username"
password = "your_password"

# Perform HTTP request with basic authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password), verify=False)  

# Check if the request was successful (status code 200)
if response.status_code == 200:
	data = response.json()
	
	# Check if the "items" key exists in the JSON
	if "items" in data:
		items = data["items"]
		print("Full Path", "Member", "Member's Port", "State", sep="\t")

		for item in items:
			fullPath = item.get("fullPath")
			
			# Check if the "membersReference" component exists in the current item
			if "membersReference" in item:
				membersReference = item.get("membersReference", {})
				link = membersReference.get("link")
				
				# Modify the content of the link
				modified_link = link.replace("localhost", "X.X.X.X")
				
				# Perform a new request using the modified URL
				response_detail = requests.get(modified_link, auth=HTTPBasicAuth(username, password), verify=False)
				
				if response_detail.status_code == 200:
					data_detail = response_detail.json()
					
					# Check if the "items" key exists in the resulting JSON
					if "items" in data:
						itemsInt = data_detail["items"]
						
						# Extract the "name" and "state" components from the resulting JSON
						for obj in itemsInt:
							fullPath_int = obj.get("fullPath")
							state = obj.get("state")
							
							# Split the member into name and port
							fullPath_parts = fullPath_int.split(":")
							fullPath_left = fullPath_parts[0]
							fullPath_right = fullPath_parts[1]
							print(fullPath + "\t" + fullPath_left + "\t" + fullPath_right + "\t" + state)
				
				else:
					print("Error obtaining details from the URL:", response_detail.status_code)
				
		print ("*" * 50)
		
	else:
		print("No 'items' elements found in the JSON.")
	
else:
    print("Error obtaining the JSON. Status code:", response.status_code)
