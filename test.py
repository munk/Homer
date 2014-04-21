import doh
import model

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
