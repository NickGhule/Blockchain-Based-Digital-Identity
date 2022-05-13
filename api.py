from flask  import Flask, render_template, request, jsonify, url_for, redirect, flash
import os
import datetime
import json
import pymongo
from bson.json_util import dumps
import hashlib

from databaseConnection import DatabaseConnection
from blockchainConnection import BlockchainConnection

app = Flask(__name__)

def ObjectId(data):
    return data

def convertTodict(data):
    output = {}
    for i,d in enumerate(data):
        output[i] = d
    return output



app.template_dir = os.path.abspath('./webpages/')

@app.route('/')
def home():
    return "ok"

@app.route('/login', methods=['GET', 'POST'])
def login():
    pass

@app.route('/view/<string:userName>/', methods=['GET', 'POST'])
def view(userName):
    db = DatabaseConnection("identityDB")
    docs = db.fetchAlldocuments(userName)
    docsSeparated = {}
    for doc in docs:
        print(doc["documentName"])
        if docsSeparated.get(doc["documentName"]) == None:
            docsSeparated[doc["documentName"]] = [doc]
        else:
            docsSeparated[doc["documentName"]].append(doc)

    print(docsSeparated)
    # return render_template('view.html', userName=userName, docsSeparated=docsSeparated)
    print(jsonify(loads(dumps(list(docsSeparated)))))
    return jsonify(loads(dumps(list(docsSeparated))))

@app.route('/view/<string:userName>/<string:documentName>/history', methods=['GET', 'POST'])
def history(userName, documentName):
    db = DatabaseConnection("identityDB")
    docs = db.fetchDocument(userName, documentName)
    # for doc in docs:
    #     print(dumps(doc))
    return jsonify(json.loads(dumps(list(docs))))

@app.route('/view/<string:shareFrom>/<string:shareTo>/<string:documentId>/share', methods=['GET', 'POST'])
def share(shareFrom, shareTo, documentId):
    db = DatabaseConnection("identityDB")
    result = db.shareDocument(shareFrom, shareTo, documentId)
    if result:
        return "success"
    else: return "failure"

@app.route('/verifier/<string:userName>/', methods=['GET', 'POST'])
def verifier(userName):
    db = DatabaseConnection("identityDB")
    shared = db.fetchShared(userName)
    docs = {}
    for i,doc in enumerate(shared):
        docs[i]= list(db.fetchDocument(doc.get("shareFrom"), doc.get("documentName")))[-1]
    
    print(dumps(docs))
    return json.loads(dumps(docs))

@app.route('/verifier/<string:userName>/<string:shareFrom>/<string:documentName>/history', methods=['GET', 'POST'])
def check_history(userName, shareFrom, documentName):
    db = DatabaseConnection("identityDB")
    docs = db.fetchShared(userName)
    # print(dumps(docs))
    for doc in docs:
        print(doc.get("shareFrom"))
        print(doc.get("documentName"))
        if doc.get("shareFrom") == shareFrom and doc.get("documentName") == documentName:
            print("pass")
            db = DatabaseConnection("identityDB")
            docs = db.fetchDocument(shareFrom, documentName)
            return jsonify(json.loads(dumps(list(docs))))
    # for doc in docs:
    #     print(dumps(doc))
    return "Not shared"

@app.route('/verifier/<string:userName>/<string:shareFrom>/<string:documentName>/verify', methods=['GET', 'POST'])
def verify(userName, shareFrom, documentName):
    db = DatabaseConnection("identityDB")
    bc = BlockchainConnection()

    hist = bc.getDocumentHistory(shareFrom, documentName)

    db = DatabaseConnection("identityDB")
    doc = list(db.fetchDocument(shareFrom, documentName))[-1]
    # bc.addDocument("nickghule", "test", hashlib.sha256(dumps(doc).encode()).hexdigest())
    if hashlib.sha256(dumps(doc).encode()).hexdigest() == hist[-1]:
        return "verified"
    else : "Not verified"
    
    
    







if __name__ == '__main__':
    app.run(debug=True)