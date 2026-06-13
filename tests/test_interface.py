from fastapi.testclient import TestClient
from herio import Interface, Textbox, Text
import pytest

def test_interface_basic():
    def dummy_fn(text):
        return f"Echo: {text}"
    
    iface = Interface(fn=dummy_fn, inputs=Textbox(), outputs=Text())
    client = TestClient(iface.app)
    
    # Test GET /
    response = client.get("/")
    assert response.status_code == 200
    assert "Herio App" in response.text
    
    # Test POST /predict
    response = client.post("/predict", json={"data": ["Hello"]})
    assert response.status_code == 200
    assert response.json() == {"data": ["Echo: Hello"]}

def test_interface_multi_input():
    def add(a, b):
        return a + b
    
    from herio import Number
    iface = Interface(fn=add, inputs=[Number(), Number()], outputs=Text())
    client = TestClient(iface.app)
    
    response = client.post("/predict", json={"data": [10, 20]})
    assert response.status_code == 200
    assert response.json() == {"data": [30.0]}
