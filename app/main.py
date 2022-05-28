from fastapi import FastAPI, Body, Depends
from .model import EmployeeSchema, UpdateEmployeeModel, UserSchema, UserLoginSchema
from .auth_bearer import JWTBearer
from .auth_handler import signJWT
from fastapi.encoders import jsonable_encoder
from .database import add_user, add_employee, delete_employee, retrieve_employees, update_employee, check_user

app = FastAPI()


@app.get("/", tags=["Root"])
async def home():
    return {"message": "Welcome to the fastapi app!"}

@app.get("/employee", response_description="employee retrieved")
async def get_employee():
    employee = retrieve_employees()
    if employee:
        return {"employee":employee, "message":"employees data retrieved successfully"}
    return {"employee":employee, "message":"Empty list returned"}

@app.post("/add_employee", dependencies=[Depends(JWTBearer())], response_description="employee data added into the database")
async def add_employee_data(employee: EmployeeSchema = Body(...)):
    employee = jsonable_encoder(employee)
    new_employee = add_employee(employee)
    return {"New employee":new_employee, "message":"employee added successfully."}

@app.put("/{emp_id}", dependencies=[Depends(JWTBearer())])
async def update_employee_data(emp_id: str, req: UpdateEmployeeModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_employee = update_employee(emp_id, req)
    if updated_employee:
        return {"message": "Updated successfully."}
    return {"message": "There was an error updating the employee data." }

@app.delete("/{emp_id}", dependencies=[Depends(JWTBearer())], response_description="employee data deleted from the database")
async def delete_employee_data(emp_id: str):
    deleted_employee = delete_employee(emp_id)
    if deleted_employee:
        return {
            "employee with ID: {} removed".format(emp_id), "employee deleted successfully"}
    return {
        "An error occurred", 404, "employee with id {0} doesn't exist".format(emp_id)
    }

@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    new_user = jsonable_encoder(user)
    add_user(new_user) # replace with db call, making sure to hash the password first
    return signJWT(user.username)


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.username)
    return {
        "error": "Wrong login details!"
    }
