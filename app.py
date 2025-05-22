#paginate data
#add ways for user to search through universities either by name or country
#different page numbers, user's page is rerouted when they click the NEXT button (going back to the pagination)
#add a segment for the next button and styling
#add segment for the rerouting
from flask import Flask, render_template
import requests

app = Flask(__name__)


#for idx, uni in enumerate(university_list)


@app.route("/")
def index():
    page = request.args.get('page', 1, type=int)
    limit = 50
    offset = (page - 1) * limit

    #fetching universities with pagination
    response = requests.get(f"http://universities.hipolabs.com/search?name={university_name}&limit={limit}&offset={offset}")
    university_list = response.json()
    #print(university_list)

   


@app.route("/universities/<int:id>")
def university_detail(id):
    response = requests.get("http://universities.hipolabs.com/search?name=har")
    #rerouting goes here (page numbers)
    university_list = response.json()







universities = [{

            'id': idx,
            'name': university.get('name', 'Unknown'),
            'country': university.get('country', 'Unknown'),
            'website': university.get('web_pages', [''])[0],
            'domains': university.get('domains', [])

        }for idx, university in enumerate(university_list):)

    if 0 <= id < len(university_list): 
        university = university_list[id]
          
    else:
        return "University not found", 404
    
return render_template("index.html", universities=universities, page=page)

if __name__ == '__main__':
    app.run(debug=True)