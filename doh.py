from flask import Flask, render_template
from flask.ext.pymongo import PyMongo
import mongolab_cred as mc

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://%s:%s@ds029267.mongolab.com:29267/nyc_restaurants" % (mc.username, mc.password)

mongo = PyMongo(app)

@app.route("/")
def hello():
    return "NYC DOH STATS"

@app.route("/stats/<int:zipcode>")
def stats(zipcode):
    rest_in_zip = mongo.db.ratings.find({'ZIPCODE': zipcode})
    return str(list(rest_in_zip))

@app.route("/view/<int:zipcode>")
def stats_view(zipcode):
    rest_in_zip = mongo.db.ratings.find({'ZIPCODE': zipcode}).sort("INSPDATE", -1)
    return render_template('dataview.html', zipcode=zipcode, data=rest_in_zip)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
