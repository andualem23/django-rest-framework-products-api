import requests

endpoint = "http://localhost:8000/api/products/" 

data = {
    "title": "Created this product",
    "price": 12.99
}

get_response = requests.post(endpoint, json=data) 
print(get_response.json())