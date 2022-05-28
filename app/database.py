import bcrypt
import pymongo

from .model import UserLoginSchema


client = pymongo.MongoClient('mongodb+srv://aman2001:yEdVL3TGJ60LMS5x@cluster0.gpgt5.mongodb.net/?retryWrites=true&w=majority')

database = client.fastapidb

employee_collection = database["employee_collection"]

user_collection = database["user_collection"]

def check_user(data: UserLoginSchema):
    data.password= bcrypt.hashpw(str(data.password).encode('utf-8'), bcrypt.gensalt())
    if user_collection.find_one({"username": data.username}):
        return True
    return False

def helper(employee) -> dict:
    return {
        "id": str(employee["_id"]),
        "emp_id": employee["emp_id"],
        "fullname": employee["fullname"],
        "email": employee["email"],
        "department": employee["department"]
    }

def helperu(user) -> dict:
    return {
        "id": str(user["_id"]),
        "fullname": user["fullname"],
        "username": user["username"],
        "password": user["password"]
    }

# Add a new employee into to the database 
def add_user(user_data: dict) -> dict:
    user_data["password"] = bcrypt.hashpw(str("password").encode('utf-8'), bcrypt.gensalt())
    user = user_collection.insert_one(user_data)
    new_user = user_collection.find_one({"_id": user.inserted_id})
    return helperu(new_user)

# Retrieve all employee present in the database
def retrieve_employees():
    employees = []
    for employee in employee_collection.find():
        employees.append(helper(employee))
    return employees


# Add a new employee into to the database
def add_employee(employee_data: dict) -> dict:
    employee =  employee_collection.insert_one(employee_data)
    new_employee = employee_collection.find_one({"_id": employee.inserted_id})
    return helper(new_employee)


# Update a employee with a matching ID
def update_employee(emp_id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    employee = employee_collection.find_one({"emp_id": emp_id})
    if employee:
        updated_employee = employee_collection.update_one(
           {"emp_id": emp_id}, {"$set": data}
        )
        if updated_employee:
            return True
        return False


# Delete a employee from the database
def delete_employee(emp_id: str):
    employee = employee_collection.find_one({"emp_id": emp_id})
    if employee:
        employee_collection.delete_one({"emp_id": emp_id})
        return True