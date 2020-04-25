from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

##############################################################
# Zadanie 1
##############################################################

def test_hello_world():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World during the coronavirus pandemic!"}


##############################################################
# Zadanie 2
##############################################################

def test_return_get():
    response = client.get('/method')
    assert response.status_code == 200
    assert response.json() == {"method": "GET"}

def test_return_post():
    response = client.post('/method')
    assert response.status_code == 200
    assert response.json() == {"method": "POST"}

def test_return_put():
    response = client.put('/method')
    assert response.status_code == 200
    assert response.json() == {"method": "PUT"}

def test_return_delete():
    response = client.delete('/method')
    assert response.status_code == 200
    assert response.json() == {"method": "DELETE"}


##############################################################
# Zadanie 3
##############################################################


##############################################################
# Zadanie 4
##############################################################


##############################################################
# Wykłąd
##############################################################


# @pytest.mark.parametrize("name", ["Ala", "Zażółć Gęślą jaźń", "Grzegorz Brzęczyszczykiewicz"])
# def test_hello_name(name):
#     response = client.get(f'/hello/{name}')
#     assert response.status_code == 200
#     assert response.json() == {"message": f"Hello {name}"}
#
# def test_receive_something():
#     response = client.post("/dej/mi/coś", json={'first_key': 'some_value'})
#     assert response.json() == {"received": {'first_key': 'some_value'},
#                                "constant_data": "python jest super"}

# def test_return_method():
#     response = client.get('/method')
#     assert response.status_code == 200
#     assert response.json() == {"message": "METHOD"}
