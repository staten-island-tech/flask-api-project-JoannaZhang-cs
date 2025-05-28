import requests    
page = 2
# name = Harv
country = "Canada"
limit = 10
offset = (page - 1) * limit


params = {
    # 'name': name,
    'page':2,
    'country': country
}

response = requests.get("http://universities.hipolabs.com/search", params=params)
paginated_universities = response.json()
print(paginated_universities)
