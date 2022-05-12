from flask  import Flask, render_template, request, jsonify, url_for, redirect, flash
import os
import datetime
import json
import pymongo
from bson.json_util import dumps

from databaseConnection import DatabaseConnection

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
    pass

# @app.route('/view/<string:userName>/<string:docID>/', methods=['GET', 'POST'])
# def view_doc(userName, docID):
#     db = DatabaseConnection("identityDB")
#     doc = db.fetchDocument(userName, docID)
#     return render_template('view_doc.html', userName=userName, doc=doc)






if __name__ == '__main__':
    app.run(debug=True)