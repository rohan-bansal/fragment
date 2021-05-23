from flask import Flask, render_template, request, url_for, redirect, abort
import logging
from logging import Formatter, FileHandler
import hashlib
import requests
import os
import markdown
import markdown.extensions.fenced_code
from markupsafe import Markup

app = Flask(__name__)
app.config.from_object('config')

def uploadText(hash_, text):

    listUrl = "https://api.airtable.com/v0/appL5PANPfvJ59eji/Links?maxRecords=3&view=Grid%20view&fields%5B%5D=hash&maxRecords=100"
    headers = {
        "Authorization" : "Bearer " + app.config['AIRTABLE_KEY'],
    }
    
    createdHashes = []
    offset = ""

    while True:
        if offset == "":
            y = requests.get(listUrl, headers=headers)
        else:
            y = requests.get(listUrl, headers=headers, json={"offset":offset})

        for element in y.json()['records']:
            createdHashes.append(element['fields']['hash'])

        if "offset" in y.json():
            offset = y.json()['offset']
        else:
            break

    if hash_ not in createdHashes:
        url = "https://api.airtable.com/v0/appL5PANPfvJ59eji/Links"
        fields = {
            "records" : [
                {
                    "fields" : {
                        "hash" : hash_,
                        "text" : text
                    }
                }
            ]
        }

        x = requests.post(url, json=fields, headers=headers)

        return x.status_code
    else:
        return 200

def getTextByRecordHash(hash_):
    listUrl = "https://api.airtable.com/v0/appL5PANPfvJ59eji/Links?maxRecords=3&view=Grid%20view&maxRecords=100"
    headers = {
        "Authorization" : "Bearer " + app.config['AIRTABLE_KEY'],
    }
    
    hashAndText = {}
    offset = ""

    while True:
        if offset == "":
            y = requests.get(listUrl, headers=headers)
        else:
            y = requests.get(listUrl, headers=headers, json={"offset":offset})

        for element in y.json()['records']:
            hashAndText[element['fields']['hash']] = element['fields']['text']

        if "offset" in y.json():
            offset = y.json()['offset']
        else:
            break
    
    if hash_ not in hashAndText:
        return -1, "None"
    else:
        return 1, hashAndText[hash_]

@app.route("/<code>")
def link(code):
    status, text = getTextByRecordHash(code)
    if status == -1:
        abort(404)
    
    md_template_string = markdown.markdown(text, extensions=['fenced_code'])
    marked_up = Markup(md_template_string)
    
    return render_template('pages/placeholder.view.html', renderText=marked_up)

@app.route("/error", methods=['POST', 'GET'])
def error():
    return render_template('errors/placeholder.error.html', error_text="Something went wrong. Try again!")


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == 'GET':
        return render_template('pages/placeholder.home.html', trigger_modal=False)
    elif request.method == 'POST':
        text = request.form['textarea-note']
        
        hashed = hashlib.md5(text.encode()).hexdigest()[:10]
        code = uploadText(hashed, text)

        if code == 200:
            return render_template('pages/placeholder.home.html', trigger_modal=True, hash_=hashed)
        else:
            return redirect(url_for('error'))

@app.errorhandler(500)
def internal_error(error):
    render_template('errors/placeholder.error.html', error_text="Code 500.")


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/placeholder.error.html', error_text="Invalid URL (404).")

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

