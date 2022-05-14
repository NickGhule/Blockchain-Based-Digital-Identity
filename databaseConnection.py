from pymongo import MongoClient
from urllib.parse import quote
from datetime import datetime

class DatabaseConnection:
    def __init__(self, dbName):
        #self.host = host
        #self.port = port
        self.dbName = dbName
        connectionString = "mongodb+srv://NickGhule:"+ quote("Nikhil@2000") +"@digital-identity-cluste.nnlnd.mongodb.net/identityDB?retryWrites=true&w=majority"
        self.client = MongoClient(connectionString)
        self.db = self.client[self.dbName]

    def getCollection(self, collectionName):
        return self.db[collectionName]
    
    def getDatabase(self):
        return self.db
    
    def getUser(self, userName):
        return self.db.userDetails.find_one({"_id": userName})
    
    def addUser(self, userName, name, password, userType):
        result = self.db.userDetails.insert_one({"_id": userName, "name": name, 
                                        "password": password, "userType": userType})
        return result.inserted_id
        
    def updateUser(self, userName, name, password, email, phoneNumber):
        result = self.db.userDetails.update_one({"_id": userName}, {"$set": {"name": name, "password": password, "email": email, "phoneNumber": phoneNumber}})
        return result.modified_count

    def deleteUser(self, userName):
        result = self.db.userDetails.delete_one({"_id": userName})
        return result.deleted_count

    def addDocument(self, userName, documentName, documentData):
        result = self.db.documentDetails.insert_one({"userName": userName, "documentName": documentName, "timestamp": datetime.now(), "documentData": documentData})
        return result.inserted_id

    def fetchDocument(self, userName, documentName):
        return self.db.documentDetails.find({"userName": userName, "documentName": documentName})

    def fetchAlldocuments(self, userName):
        return self.db.documentDetails.find({"userName": userName})

    def shareDocument(self, shareFrom, shareTo, documentId):
        result = self.db.shareDetails.insert_one({"shareFrom": shareFrom, "shareTo": shareTo, "documentName": documentId})
        return result.inserted_id
    
    def fetchShared(self, userName):
        return self.db.shareDetails.find({"shareTo": userName})
    
    

if __name__ == '__main__':
    db = DatabaseConnection("identityDB")
    print(db.addUser("nickghule", "Nikhil Ghule", "nikhil", 2))
    # print(db.getUser("nickghule2"))
    # print(db.addDocument("nickghule", "other", "doc2"))
    # docs = db.fetchDocument("nickghule", "other")
    # docs = db.fetchAlldocuments("nickghule")
    # for doc in docs:
    #     print(doc)