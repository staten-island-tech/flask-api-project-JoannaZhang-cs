from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def index():
    page = request.args.get('page', 1, type=int)
    limit = 100
    offset = (page - 1) * limit
    #page=current page number & limit=number of items displayed per page & offset=how many items to skip before getting data for current page/page thats needed
    
    #to get subset of records for pagination
    #optional: change this to a query parameter or default search keyword
    university_name = request.args.get("name", "harvard")

    #fetching universities with pagination
    response = requests.get(f"http://universities.hipolabs.com/search?name={university_name}")
    university_list = response.json()

    #apply manual pagination (API doesn't support offset & limit natively)
    paginated_universities = university_list[offset:offset + limit]

    universities = [{
        'id': idx + offset,  # Ensures unique ID across pages
        'name': university.get('name', 'Unknown'),
        'country': university.get('country', 'Unknown'),
        'website': university.get('web_pages', [''])[0],
        'domains': university.get('domains', [])
    } for idx, university in enumerate(paginated_universities)]

    return render_template("university.html", universities=universities, page=page)


@app.route("/universities/<int:id>")
def university_detail(id):
    # Again, example assumes 'harvard' search (or could cache the results)
    response = requests.get("http://universities.hipolabs.com/search?name=harvard")
    university_list = response.json()

    if 0 <= id < len(university_list):
        university = university_list[id]
        return render_template("detail.html", university=university)
    else:
        return "University not found", 404


if __name__ == '__main__':
    app.run(debug=True)