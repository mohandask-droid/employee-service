import json

import pytest
from fastapi.testclient import TestClient

from src import main

SAMPLE = [
    {"name": "Arun", "department": "Sales", "salary": 30000},
    {"name": "Divya", "department": "IT", "salary": 75000},
]


@pytest.fixture
def client(tmp_path, monkeypatch):
    data_file = tmp_path / "employees.json"
    data_file.write_text(json.dumps(SAMPLE))
    monkeypatch.setattr(main, "DATA_FILE", data_file)
    return TestClient(main.app)


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_list_employees(client):
    r = client.get("/employees")
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_get_employee_success(client):
    r = client.get("/employees/Arun")
    assert r.status_code == 200
    assert r.json()["name"] == "Arun"


def test_get_employee_404(client):
    assert client.get("/employees/Ravi").status_code == 404


def test_create_employee_success(client):
    r = client.post("/employees", json={"name": "Ravi", "salary": 50000})
    assert r.status_code == 201
    assert len(client.get("/employees").json()) == 3


def test_invalid_salary(client):
    r = client.post("/employees", json={"name": "Ravi", "salary": -5})
    assert r.status_code == 422


def test_empty_name(client):
    r = client.post("/employees", json={"name": "", "salary": 1000})
    assert r.status_code == 422
