import pytest
import requests
from models import Fruit, db
from app import app

def test_route_home_test_client():
	client = app.test_client()
	response = client.get('/')
	assert response.status_code == 200

def test_route_home_pythonanywhere():
    response = requests.get("https://ramia128.pythonanywhere.com/")
    assert response.status_code == 200

def test_vitaminA():
    with app.app_context():
        data = Fruit.query.order_by((getattr(Fruit, "Vitamin_A_RE_per_mikrog")).desc()).limit(10).first() 

    assert data.Namn == "Morot"

def test_vitaminA_online():
     client = app.test_client()
     response = client.get('/vitaminer/Vitamin A')
     assert response.status_code == 200

     with app.app_context():
        data = Fruit.query.order_by((getattr(Fruit, "Vitamin_A_RE_per_mikrog")).desc()).limit(10).all() 

     for element in data:
        assert element.Namn in response.text


