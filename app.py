from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)


@app.route("/")
def index():
    page = request.args.get('page', default= 1, type=int)
    name = request.args.get('name', default='Toronto', type=str)
    country = request.args.get('country', default = 'Canada', type=str)
    limit = 10
    offset = (page - 1) * limit

    
    params = {
        'name': name,
        'country': country,
        'page' : page,
    }

    response = requests.get("http://universities.hipolabs.com/search?", params=params)
    paginated_universities = response.json()
    print(paginated_universities)
    

    total = len(paginated_universities)
    paginated_universities = paginated_universities[offset:offset + limit]

    paginated_universities = [{
        'id': idx + offset,  
        'name': university.get('name', 'Unknown'),
        'country': university.get('country', 'Unknown'),
        'website': university.get('web_pages', [''])[0],
        'domains': university.get('domains', [])
    } for idx, university in enumerate(paginated_universities)]


    return render_template(
        "index.html",
        universities=paginated_universities,
        page=page,
        total=total,
        limit=limit,
        name=name,
        country=country
    )
    


@app.route("/universities/<int:id>")
def university_detail(id):
    response = requests.get("http://universities.hipolabs.com/search?name=harvard")
    university = response.json()

    if 0 <= id < len(university):
        university = university[id]
        return render_template("university.html", university=university)
    else:
        return "University not found", 404


if __name__ == '__main__':
    app.run(debug=True)