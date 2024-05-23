import pytest
import requests
from models import Fruit, db
from app import app


def test_route_home_local():
    response = requests.get('http://127.0.0.1:5000')
    assert response.status_code == 200

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
    response = requests.get('http://127.0.0.1:5000/vitaminer/Vitamin A')
    assert response.status_code == 200

    with app.app_context():
        data = Fruit.query.order_by((getattr(Fruit, "Vitamin_A_RE_per_mikrog")).desc()).limit(10).first() 

    print(data.Namn, type(response.text))

    assert "Morot" in response.text


