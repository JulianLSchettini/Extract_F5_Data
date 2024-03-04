import requests
from requests.auth import HTTPBasicAuth

url = "https://X.X.X.X/mgmt/tm/net/self"
username = "tu_user"
password = "tu_password"

# Perform HTTP request with basic authentication
response = requests.get(url, auth=HTTPBasicAuth(username, password), verify=False)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()

    # Check if the key "items" exists in the JSON
    if "items" in data:
        items = data["items"]
        print("Full Path", "Address", "Traffic Group", "Port Lock", sep="\t")
        # Iterate over the components of items.
        for item in items:
            fullPath = item.get("fullPath")
            address = item.get("address")
            trafficGroup = item.get("trafficGroup")
            allowService = item.get("allowService")

            # Check if 'allowService' is a list
            if isinstance(allowService, list):
                # Convert the list to a comma-separated string
                allowService_str = ",".join(allowService)

            else:
                # If 'allowService' is not a list, simply convert it to a string
                allowService_str = str(allowService)

            # Print the data, ensuring to use 'allowService_str' instead of 'allowService'
            print(fullPath + "\t" + address + "\t" + trafficGroup + "\t" + allowService_str)

    else:
        print("No 'items' elements found in the JSON.")
else:
    print("Error retrieving JSON. Status code:", response.status_code)