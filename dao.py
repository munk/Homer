from cuisine import res

class GradeDAO(object):
    groupby = {"$group":
        {"_id":
            {"camis": "$CAMIS",
             "dba": "$DBA",
             "phone": "$PHONE",
             "grade": "$CURRENTGRADE"},
         "RECORDDATE": {"$max":"$RECORDDATE"}
        }
    }
    borodict = {"manhattan": 1,
              "brooklyn": 3,
              "queens": 4,
              "statenisland": 5,
              "thebronx": 2}

    def __init__(self, mongo):
        self.ratings = mongo.db.ratings

    def __get_grades__(self, match, groupby=groupby):
        resultset = self.ratings.aggregate([match, groupby])
        return resultset['result']

    def get_grade_by_zipcode(self, key):
        match = {"$match": {"ZIPCODE": key}}
        return self.__get_grades__(match)

    def get_grade_by_boro(self, key):
        match = {"$match": {"BORO": boro[key]}}
        return self.__get_grades__(match)

    def get_grade_by_cuisine(self, key):
        match = {"%match": {"CUISINE": key}}
        return self.__get_grades__(match)

    def get_grade_by_phone(self, key):
        match = {"$match": {"PHONE": key}}
        groupby = {
            "$group":{"_id":
                         {"insp_id" : "$_id",
                          "camis": "$CAMIS",
                          "dba": "$DBA",
                          "score": "$SCORE",
                          "cuisine": "$CUISINECODE",
                          "violation": "$VIOLCODE",
                          "grade": "$CURRENTGRADE",
                          "building": "$BUILDING",
                          "street": "$STREET",
                          "boro": "$BORO",},
                    "INSPECTIONDATE": {"$max":"$INSPDATE"}}}
        return self.__get_grades__(match, groupby)

    def get_summary(self, boro, cuisine=False):
        query = {'BORO': self.borodict[boro]}
        if cuisine:
            query['CUISINECODE'] = res[cuisine]
        camis = self.ratings.find(query).distinct('CAMIS')
        result = self.ratings.find({'CAMIS': {"$in": camis}})
        return result
