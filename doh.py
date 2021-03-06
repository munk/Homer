from flask import Flask, render_template, request, redirect, url_for, flash
from flask.ext.pymongo import PyMongo
import model
from cuisine import cuisine_codes
from violation import violations as vl
from flask.ext.googlemaps import GoogleMaps
from flask.ext.googlemaps import Map
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)
uri = "mongodb://%s:%s@ds049558.mongolab.com:49558/nyc_restaurants"
app.config['MONGO_URI'] = uri  % (os.environ.get('mongolab_username'),
                                  os.environ.get('mongolab_password'))

GoogleMaps(app)
mongo = PyMongo(app)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/search", methods=["POST"])
def search():
    query = request.form.get('q')
    print(query)
    print("in search")
    if query is None:
        return redirect(url_for("hello"))
    elif model.is_zipcode(query):
        print ("is zipcode")
        return render_template('dataview.html',
                   zipcode=query,
                   data=model.get_grades(int(query), mongo))
    elif model.is_phone_number(query):
        print("is phone")
        business = model.get_business(query, mongo)
        if business is None:
            flash("Business not found")
            return redirect(url_for("hello"))
        mymap = Map(
            identifier="view-side",
            lat=business.geocode.coordinates[0],
            lng=business.geocode.coordinates[1],
        )
        return render_template("search.html",
                               restaurant=business,
                               mymap=mymap)
    else:
        return redirect(url_for("hello"))

@app.route("/browse", methods=["GET", "POST"])
def browse():
    if request.method == 'POST':
        requested_boro = request.form['boro']
        requested_cuisine = cuisine_codes.get(int(request.form['cuisine']), False)
        data = model.get_summary(requested_boro, requested_cuisine, mongo)
        violations = []
        viol_grp = data.groupby('VIOLCODE')
        violations = [(vl.get(name, "Unknown"), frame.CAMIS.count()) for name, frame in viol_grp]

        return render_template('summary.html', cuisine=requested_cuisine, boro=requested_boro, data=data, violations=violations)
    return render_template('browse.html', cuisine_codes=cuisine_codes)

@app.route("/stats/<int:zipcode>")
def stats(zipcode):
    return str(model.get_grades(zipcode, mongo))

@app.route("/view/<kind>/<key>")
def stats_view(kind, key):
    return render_template('dataview.html',
                           key=key,
                           kind=kind,
                           data=model.get_grades(key, mongo, kind=kind))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
