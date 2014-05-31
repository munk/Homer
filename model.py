from restaurant import Restaurant
from cuisine import res
from dao import GradeDAO
import pandas as pd

boro = {"manhattan": 1,
              "brooklyn": 3,
              "queens": 4,
              "statenisland": 5,
              "thebronx": 2}


def ga et_grades(key, mongo, kind="zipcode"):
    """Retrieve grades grouped by key"""
    dao = GradeDAO(mongo)
    if kind == "zipcode":
        return dao.get_grade_by_zipcode(key)
    elif kind == "boro":
        return dao.get_grade_by_boro(key)
    else:
        return dao.get_grade_by_cuisine(key)


def get_summary(boro, cuisine, mongo):
    dao = GradeDAO(mongo)
    boro = boro.replace(' ', '').lower()
    result = dao.get_summary(boro, cuisine)
    if not result:
        return "No results found"

    df = pd.DataFrame([r for r in result])
    keys = df.groupby('CAMIS')['INSPDATE'].transform(max) == df.INSPDATE
    have_grades =  df[keys].dropna(subset=['CURRENTGRADE'])
    return have_grades


def get_business(phone, mongo):
    dao = GradeDAO(mongo)
    result = dao.get_grade_by_phone(phone)
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
