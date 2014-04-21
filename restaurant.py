class Restaurant(object):
    def __init__(self, data):
        inspection_date = data[0]['INSPECTIONDATE']
        grade = data[0]['_id']['grade']
        camis = data[0]['_id']['camis']
        cuisine = data[0]['_id']['cuisine']
        score = data[0]['_id']['score']
        violations = [d['_id']['violation'] for d in data]

    def __repr__(self):
        result = "CAMIS: " + self.camis + \
                 "\nGrade: " + self.grade + \
                 "\nCuisine: " + self.cuisine + \
                 "\nScore: " + self.score + \
                 "\nViolations: " + '\n'.join(self.violations) 
    def __str__(self):
        return self.__repr__()
       
