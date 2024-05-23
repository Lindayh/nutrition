import pytest
import requests
from models import Fruit, db


def test_route_home_local():
    response = requests.get('http://127.0.0.1:5000')
    assert response.status_code == 200

def test_route_home_pythonanywhere():
    response = requests.get("https://ramia128.pythonanywhere.com/")
    assert response.status_code == 200

def test_vitaminA():
    response = requests.get('http://127.0.0.1:5000/vitaminer/Vitamin A')

    # Test in some way that you get vitamin A stuff

    # Query database
    data = Fruit.query.order_by((getattr(Fruit, "Vitamin_A_RE_per_mikrog")).desc()).limit(10).all() 


    print(response)

