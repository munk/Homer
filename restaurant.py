class Restaurant(object):
    def __init__(self, data):
        self.inspection_date = data[0]['INSPECTIONDATE']
        self.grade = data[0]['_id']['grade']
        self.camis = data[0]['_id']['camis']
        self.cuisine = data[0]['_id']['cuisine']
        self.score = data[0]['_id']['score']
        self.violations = [d['_id']['violation'] for d in data]

        if self.grade == 'Z':
            self.grade = "Pending"

    def __repr__(self):
        result = "CAMIS: " + str(self.camis) + \
                 "\nGrade: " + self.grade + \
                 "\nCuisine: " + str(self.cuisine) + \
                 "\nScore: " + str(self.score) + \
                 "\nViolations: " + '\n'.join(self.violations) 
        return result

    def __str__(self):
        return self.__repr__()
       
