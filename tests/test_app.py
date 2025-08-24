# tests/test_app.py
import pytest
from flask import Flask, render_template, request, jsonify, json, make_response, Response, send_from_directory

@pytest.fixture
def client():
    app = Flask(__name__) # create_app()
    with app.test_client() as client:
        yield client

def test_hello_world(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello, World!" in response.data