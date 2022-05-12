from flask  import Flask, render_template, request, jsonify, url_for, redirect, flash
import os

from databaseConnection import DatabaseConnection

app = Flask(__name__)


app.template_dir = os.path.abspath('./webpages/')

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

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
    return render_template('view.html', userName=userName, docsSeparated=docsSeparated)

@app.route('/view/<string:userName>/<string:docID>/', methods=['GET', 'POST'])
def view_doc(userName, docID):
    db = DatabaseConnection("identityDB")
    doc = db.fetchDocument(userName, docID)
    return render_template('view_doc.html', userName=userName, doc=doc)






if __name__ == '__main__':
    app.run(debug=True)