import doh
import model
import restaurant

def test_home():
    app = doh.app.test_client()
    assert 'input type="search"' in str(app.get('/').data)

def test_valid_phone_number():
    assert model.is_phone_number('1235551234')

def test_valid_phone_number_with_dashes():
    assert model.is_phone_number('123-555-1234')
    
def test_valid_phone_number_with_parens():
    assert model.is_phone_number('(123) 555-1234')

def test_valid_zipcode():
    assert model.is_zipcode('12345')

def test_new_restaurant():
    data = [{"INSPECTIONDATE": 1,
            "_id": {
             "grade": 2,
             "camis": 3,
             "cuisine": 4,
             "score": 5,
             "violation": [6, 7, 8]}}]
    rest = restaurant.Restaurant(data)
    assert rest.inspection_date == 1
    assert rest.grade == 2
    assert rest.camis == 3
    assert rest.cuisine == 4
    assert rest.score == 5
    assert rest.violations == [[6, 7, 8]], rest.violations
 
