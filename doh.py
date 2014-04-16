from flask import Flask, render_template
from flask.ext.pymongo import PyMongo
import mongolab_cred as mc

app = Flask(__name__)

uri = "mongodb://%s:%s@ds029267.mongolab.com:29267/nyc_restaurants"
app.config['MONGO_URI'] = uri  % (mc.username, mc.password)

mongo = PyMongo(app)

def get_grades(zipcode):
    match = {"$match": {"ZIPCODE": zipcode}}
    groupby = {"$group":
        {"_id":
            {"camis": "$CAMIS", 
             "dba": "$DBA", 
             "grade": "$CURRENTGRADE"}, 
         "RECORDDATE": {"$max":"$RECORDDATE"}
        }
     }
    rest_in_zip = mongo.db.ratings.aggregate([match, groupby])
    return rest_in_zip['result']

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/stats/<int:zipcode>")
def stats(zipcode):
    return str(get_grades(zipcode))

@app.route("/view/<int:zipcode>")
def stats_view(zipcode):
    return render_template('dataview.html', 
                           zipcode=zipcode, 
                           data=get_grades(zipcode))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
