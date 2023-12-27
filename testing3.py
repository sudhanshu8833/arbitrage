import requests

def get_public_ip_address():
    try:
        # Use ipinfo.io to get the public IP address
        response = requests.get('https://ipinfo.io')
        ip_address = response.json()['ip']
        return ip_address
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

# Get and print the public IP address
public_ip_address = get_public_ip_address()

if public_ip_address:
    print(f"The public IP address is: {public_ip_address}")
else:
    print("Failed to retrieve the public IP address.")