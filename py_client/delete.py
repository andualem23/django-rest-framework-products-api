import requests

product_id = input('what is the id of the product you want to use?\n')

try:
    product_id = int(product_id)
except:
    product_id = None
   
if product_id: 
    
    endpoint = f"http://localhost:8000/api/products/{product_id}/delete" 

    get_response = requests.delete(endpoint) 
    print(get_response)