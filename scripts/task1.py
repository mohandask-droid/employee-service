def calculate_bonus(salary, rate=0.1, *extras, **options):
    bonus = salary * rate + sum(extras)
    if "cap" in options and bonus > options["cap"]:
        bonus = options["cap"]
    return bonus


def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def get_details(self):
        return f"{self.name} - {self.salary}"

    @property
    def annual_salary(self):
        return self.salary * 12


class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    @log_call
    def get_details(self):
        return f"{self.name} - {self.salary} - Team Size: {self.team_size}"


employees = [
    ("Arun", 30000),
    ("Priya", 45000),
    ("Rahul", 60000),
    ("Divya", 75000),
    ("Karthik", 90000),
]

for name, salary in employees:
    if salary < 50000:
        print(f"{name} - Low Salary")
    elif salary < 70000:
        print(f"{name} - Medium Salary")
    else:
        print(f"{name} - High Salary")

manager = Manager("Divya", 75000, 5)
print(manager.get_details())
