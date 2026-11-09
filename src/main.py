import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

app = FastAPI()
DATA_FILE = Path(__file__).parent.parent / "employees.json"


class Employee(BaseModel):
    name: str
    department: str = "General"
    salary: float

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name must not be empty")
        return v

    @field_validator("salary")
    @classmethod
    def salary_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("salary must be above 0")
        return v


def load_employees() -> list:
    return json.loads(DATA_FILE.read_text())


def save_employees(data: list) -> None:
    DATA_FILE.write_text(json.dumps(data, indent=2))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/employees")
def list_employees():
    return load_employees()


@app.get("/employees/{name}")
def get_employee(name: str):
    for emp in load_employees():
        if emp["name"].lower() == name.lower():
            return emp
    raise HTTPException(status_code=404, detail="Employee not found")


@app.post("/employees", status_code=201)
def create_employee(employee: Employee):
    data = load_employees()
    data.append(employee.model_dump())
    save_employees(data)
    return employee
