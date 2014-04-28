from restaurant import Restaurant

boro = {"manhattan": 1, 
              "brooklyn": 3, 
              "queens": 4,
              "statenisland": 5, 
              "thebronx": 2}

def get_grades(key, mongo, kind="zipcode"):
    match = {}
    if kind == "zipcode":
        match = {"$match": {"ZIPCODE": key}}
    elif kind == "boro":
        match = {"$match": {"BORO": boro[key]}}
    else:
        match = {"%match": {"CUISINE": key}}
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

def get_business(phone, mongo):
    match = {"$match": {"PHONE": phone}}
    groupby = {"$group":
        {"_id":
            {"insp_id" : "$_id",
             "camis": "$CAMIS", 
             "dba": "$DBA", 
             "score": "$SCORE", 
             "cuisine": "$CUISINECODE", 
             "violation": "$VIOLCODE",
             "grade": "$CURRENTGRADE"}, 
         "INSPECTIONDATE": {"$max":"$INSPDATE"},
        }
    }
    rest_in_zip = mongo.db.ratings.aggregate([match, groupby])
    result = rest_in_zip['result']
    if not result:
        return None
    max_date = max([r['INSPECTIONDATE'] for r in result]) 
    latest = filter(lambda r: r['INSPECTIONDATE'] == max_date, result)
    return Restaurant(list(latest))

def is_phone_number(number):
    number_reduced = number.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
    try:
        int(number_reduced)
        return len(number_reduced) == 10
    except ValueError:
        return False

def is_zipcode(zipcode):
    try:
        int(zipcode)
        return len(zipcode) == 5
    except ValueError:
        return False

