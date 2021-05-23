from flask import Flask, render_template, request, url_for
import logging
from logging import Formatter, FileHandler
import hashlib
import requests
import os

app = Flask(__name__)
app.config.from_object('config')

def uploadText(hash_, text):

    listUrl = "https://api.airtable.com/v0/appL5PANPfvJ59eji/Links?maxRecords=3&view=Grid%20view&fields%5B%5D=hash&maxRecords=100"
    headers = {
        "Authorization" : "Bearer " + app.config['AIRTABLE_KEY'],
        # "Content-Type" : "application/json"
    }
    
    createdHashes = []
    offset = ""

    while True:
        if offset == "":
            y = requests.get(listUrl, headers=headers)
        else:
            y = requests.get(listUrl, headers=headers, json={"offset":offset})

        print(y.json())

        for element in y.json()['records']:
            createdHashes.append(element['fields']['hash'])

        if "offset" in y.json():
            offset = y.json()['offset']
        else:
            break

    print(createdHashes, hash_)

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


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == 'GET':
        return render_template('pages/placeholder.home.html')
    elif request.method == 'POST':
        text = request.form['textarea-note']
        
        hashed = hashlib.md5(text.encode()).hexdigest()[:10]
        code = uploadText(hashed, text)

        if code == 200:
            return render_template('pages/placeholder.home.html')
        else:
            return url_for('error')

@app.route('/error')
def error():
    return render_template('errors/placeholder.error.html')


@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

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

