from config.dbconnect import connect
from datetime import datetime
db=connect()
def history_py(userid:str,topic:str,core:str):
    collection=db['history']
    d=datetime.utcnow()
    print(d)
    collection.insert_one({"userid":userid,"topic":topic,"createdAt":d,"core":core})
    return {"message":"success","status":200}
def history_get(userid:str):
    collection = db["history"]

    history = list(
        collection.find(
            {"userid": userid},
               {"_id": 0}  
        ).sort("createdAt")
    )

    return history
