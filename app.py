#paginate data
# add ways for user to search through universities either by name or country
from flask import Flask, render_template
import requests

app = Flask(__name__)

response = requests.get("http://universities.hipolabs.com/search?name=har")
university_list = response.json()
print(university_list)

@app.route("/")
def index():
   
    response = requests.get("http://universities.hipolabs.com/search?country=unitedstates")
    university_list = response.json()
    universities = []
    for idx, university in enumerate(university_list):
        universities.append({
            'id': idx,
            'name': university.get('name', 'Unknown'),
            'country': university.get('country', 'Unknown'),
            'website': university.get('web_pages', [''])[0]
        })

    return render_template("index.html", universities=universities)

@app.route("/universities/<int:id>")
def university_detail(id):
    response = requests.get("http://universities.hipolabs.com/search?name=har")
    university_list = response.json()

    if 0 <= id < len(university_list): 
        university = university_list[id]
        return render_template("university.html", university={
            'name': university.get('name', 'Unknown'),
            'country': university.get('country', 'Unknown'),
            'website': university.get('web_pages', [''])[0],
            'domains': university.get('domains', [])
        })
    else:
        return "University not found", 404

if __name__ == '__main__':
    app.run(debug=True)