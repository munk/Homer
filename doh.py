from flask import Flask, render_template, request, redirect, url_for, flash
from flask.ext.pymongo import PyMongo
import mongolab_cred as mc
import model

app = Flask(__name__)

app.secret_key = "some_secret"
uri = "mongodb://%s:%s@ds029267.mongolab.com:29267/nyc_restaurants"
app.config['MONGO_URI'] = uri  % (mc.username, mc.password)

mongo = PyMongo(app)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/search", methods=["POST"])
def search():
    query = request.form.get('q')
    if query is None:
        return redirect(url_for("hello"))
    elif model.is_zipcode(query):
        return render_template('dataview.html',
                   zipcode=query,
                   data=model.get_grades(int(query), mongo))
    elif model.is_phone_number(query):
        business = model.get_business(query, mongo)
        if business is None:
            flash("Business not found")
            return redirect(url_for("hello"))
        return render_template("search.html",
                               restaurant=business)
    else:
        return redirect(url_for("hello"))

@app.route("/browse")
@app.route("/browse/<boro>")
def browse(boro=None):
    if boro is None:
        return render_template('browse.html')
    else:
        return boro

@app.route("/stats/<int:zipcode>")
def stats(zipcode):
    return str(get_grades(zipcode, mongo))

@app.route("/view/<int:zipcode>")
def stats_view(zipcode):
    return render_template('dataview.html', 
                           zipcode=zipcode, 
                           data=get_grades(zipcode, mongo))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
