from pymongo import MongoClient
from config.dbconnect import connect
db=connect()
def login_check(email:str,passw:str):
    collection=db['login']

    print("Email:", email)
    print("Password:", passw)
    user = collection.find_one({"email": email,"password":passw})
    print("User from DB:", user)
    if user:
        return {"message":"success","status":"200","name":user["name"],"class":user["class"],"user_id": str(user["_id"])}
    else :
        return {"message":"failure","status":"500"}
