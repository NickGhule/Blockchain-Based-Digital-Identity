from urllib import response
from xml.dom import UserDataHandler
from flask import Flask, render_template, request, jsonify, url_for, redirect, flash
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
    for i, d in enumerate(data):
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
    # for doc in docs:
    # print(doc)
    docsSeparated = {}
    for doc in docs:
        print(doc["documentName"])
        if docsSeparated.get(doc["documentName"]) == None:
            docsSeparated[doc["documentName"]] = [doc]
        else:
            docsSeparated[doc["documentName"]].append(doc)

    print(docsSeparated)
    # return render_template('view.html', userName=userName, docsSeparated=docsSeparated)
    # docsSeparated = {'test': [{'_id': ObjectId('62709529f3b89ef4bfca24bb'), 'userName': 'nickghule', 'documentName': 'test', 'timestamp': datetime.datetime(2022, 5, 3, 8, 6, 25, 759000), 'documentData': {'no': '121212', 'hiii': '55555'}}, {'_id': ObjectId('627cc31dc35ad85d4a9c80a6'), 'userName': 'nickghule', 'documentName': 'test', 'timestamp': datetime.datetime(2022, 5, 13, 8, 6, 25, 759000), 'documentData': {'no': '121212', 'hiii': '55555'}}], 'doc 2': [
    #     {'_id': ObjectId('627cc332c35ad85d4a9c80a7'), 'userName': 'nickghule', 'documentName': 'doc 2', 'timestamp': datetime.datetime(2022, 5, 13, 8, 6, 25, 759000), 'documentData': {'no': '121212', 'hiii': '55555'}}], 'Doc 3': [{'_id': ObjectId('627cd4f30d8e9aaa07c60705'), 'userName': 'nickghule', 'documentName': 'Doc 3', 'timestamp': datetime.datetime(2022, 5, 3, 8, 6, 25, 759000), 'documentData': {'Attr1': 'Val 1', 'Attr2': 'Val 2'}}]}
    response = jsonify(json.loads(dumps((docsSeparated))))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/view/<string:userName>/<string:documentName>/history', methods=['GET', 'POST'])
def history(userName, documentName):
    db = DatabaseConnection("identityDB")
    docs = db.fetchDocument(userName, documentName)
    # for doc in docs:
    #     print(dumps(doc))
    response = jsonify(json.loads(dumps((docs))))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/view/<string:shareFrom>/<string:shareTo>/<string:documentId>/share', methods=['GET', 'POST'])
def share(shareFrom, shareTo, documentId):
    db = DatabaseConnection("identityDB")
    result = db.shareDocument(shareFrom, shareTo, documentId)
    if result:
        response = jsonify(json.loads(dumps(({'status': True}))))
    else:
        response = jsonify(json.loads(
            dumps(({'status': False, 'msg': "you messed up something"}))))

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/verifier/<string:userName>/', methods=['GET', 'POST'])
def verifier(userName):
    db = DatabaseConnection("identityDB")
    shared = db.fetchShared(userName)
    docs = {}
    for i, doc in enumerate(shared):
        docs[i] = list(db.fetchDocument(
            doc.get("shareFrom"), doc.get("documentName")))[-1]

    print(dumps(docs))
    # docs = {"0": {"_id": {"$oid": "627cc31dc35ad85d4a9c80a6"}, "userName": "nickghule", "documentName": "test", "timestamp": {"$date": "2022-05-13T08:06:25.759Z"}, "documentData": {"no": "121212", "hiii": "55555"}},
    #         }
    response = jsonify(json.loads(dumps((docs))))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    # return json.loads(dumps(docs))


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


@app.route('/verifier/<string:shareFrom>/<string:documentName>/verify', methods=['GET', 'POST'])
def verify(shareFrom, documentName):
    db = DatabaseConnection("identityDB")
    bc = BlockchainConnection()
    hist = bc.getDocumentHistory(shareFrom, documentName)
    db = DatabaseConnection("identityDB")
    doc = list(db.fetchDocument(shareFrom, documentName))[-1]
    # bc.addDocument("nickghule", "test", hashlib.sha256(dumps(doc).encode()).hexdigest())
    if hashlib.sha256(dumps(doc).encode()).hexdigest() == hist[-1]:
        response = jsonify(json.loads(dumps(({'varified': True}))))
    else:
        response = jsonify(json.loads(dumps(({'varified': False}))))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/issuer/<string:doc>', methods=['GET', 'POST'])
def issue(doc):
    data = json.loads(doc)
    userName = data.get("username")
    documentName = data.get("documentName")
    rawdocumentData = data.get("values")
    db = DatabaseConnection("identityDB")
    bc = BlockchainConnection()
    # TODO : check if document already exists
    # TODO : check if user exists
    doc = json.loads(doc)
    if not len(rawdocumentData):
        response = jsonify(json.loads(dumps(({'issued': False}))))
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    print("pass")

    documentData = {}
    for doc in rawdocumentData:
        documentData[doc.get("key")] = doc.get("value")
    db.addDocument(userName, documentName, documentData)

    doc = list(db.fetchDocument(userName, documentName))[-1]
    bc.addDocument(userName, documentName, hashlib.sha256(
        dumps(doc).encode()).hexdigest())

    response = jsonify(json.loads(dumps(({'issued': True}))))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/login/<string:userName>/<string:passwd>/', methods=['GET', 'POST'])
def login_user(userName, passwd):
    db = DatabaseConnection("identityDB")
    userDetail = db.getUser(userName)
    if len(userDetail) == 0:
        response = jsonify(json.loads(dumps(({'status': False}))))
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        if userDetail.get("password") == passwd:
            response = jsonify(json.loads(
                dumps(({'status': True, 'userType': userDetail.get('userType')}))))
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        else:
            response = jsonify(json.loads(dumps(({'status': False}))))
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response


@app.route('/register/<string:userName>/<string:passwd>/<int:type>/<string:name>/', methods=['GET', 'POST'])
def register_user(userName, passwd, type, name):
    db = DatabaseConnection("identityDB")
    userDetail = db.getUser(userName)
    if userDetail:
        response = jsonify(json.loads(
            dumps(({'status': False, "msg": "username is taken"}))))
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:

        db.addUser(userName, name, passwd, type)
        response = jsonify(json.loads(dumps(({'status': True}))))
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


if __name__ == '__main__':
    app.run(debug=True)
