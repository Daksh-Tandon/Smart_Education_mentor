from pymongo import MongoClient
def connect():

        client = MongoClient("mongodb://localhost:27017/")
        mydb = client["smarteducation"]
       
        return mydb

        


    
