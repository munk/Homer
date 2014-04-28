from violation import violations
from cuisine import cuisine_codes

class Restaurant(object):
    def __init__(self, data):
        self.inspection_date = data[0]['INSPECTIONDATE']
        self.grade = data[0]['_id']['grade']
        self.camis = data[0]['_id']['camis']
        self.dba = data[0]['_id']['dba']
        self.cuisine = cuisine_codes[int(data[0]['_id']['cuisine'])]
        self.score = data[0]['_id']['score']
        self.violations = []

        for v in [d['_id']['violation'] for d in data]:
            self.violations.append(violations[v])
    
        if self.grade == 'Z':
            self.grade = "Pending"

    def __repr__(self):
        result = "CAMIS: " + str(self.camis) + \
                 "\nDBA: " + self.dba + \
                 "\nGrade: " + self.grade + \
                 "\nCuisine: " + str(self.cuisine) + \
                 "\nScore: " + str(self.score) + \
                 "\nViolations: " + '\n'.join(self.violations) 
        return result

    def __str__(self):
        return self.__repr__()

