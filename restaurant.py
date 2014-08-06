from violation import violations
from cuisine import cuisine_codes
from pygeocoder import Geocoder

class Restaurant(object):
    def __init__(self, data):
        boro = {1: 'manhattan', 2: 'the bronx', 3: 'brooklyn', 4: 'queens', 5: 'staten island'}
        self.inspection_date = data[0]['INSPECTIONDATE']
        self.grade = data[0]['_id']['grade']
        self.camis = data[0]['_id']['camis']
        self.dba = data[0]['_id']['dba']
        self.cuisine = cuisine_codes[int(data[0]['_id']['cuisine'])]
        self.score = data[0]['_id']['score']
        self.violations = []
        self.address = ' '.join([data[0]['_id']['building'],
                                data[0]['_id']['street'],
                                boro[data[0]['_id']['boro']],
                                str(int(data[0]['_id']['zipcode']))])
        self.geocode = Geocoder.geocode(self.address)

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

