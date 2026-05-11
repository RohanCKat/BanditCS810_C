import requests

# B113: No timeout specified
def get_api_data(url):
    return requests.get(url)