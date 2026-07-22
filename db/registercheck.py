from config.dbconnect import connect
db=connect()
def reg_check(param:dict):
    collection=db['login']
    collection.insert_one(param)
    print("data added to the collection")
    return {"message":"success","status":200}
