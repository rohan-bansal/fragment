from flask import Flask, render_template, request, url_for, redirect, abort, send_from_directory, session
import logging
from logging import Formatter, FileHandler
import hashlib
import requests
import os
import atexit
import markdown
import markdown.extensions.fenced_code
from markupsafe import Markup
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

app = Flask(__name__, static_folder='static')
app.config.from_object('config')

scheduler = BackgroundScheduler(daemon=True)
atexit.register(lambda: scheduler.shutdown())
scheduler.start()

def deleteRecord(id_):
    deleteUrl = "https://api.airtable.com/v0/appL5PANPfvJ59eji/Links/" + id_
    headers = {
        "Authorization" : "Bearer " + app.config['AIRTABLE_KEY'],
    }

    x = requests.delete(deleteUrl, headers=headers)
    print('record ID ' + id_ + ' deleted with status code ' + str(x.status_code))

    return x.status_code

def uploadText(hash_, text, explode, explode_input):

    listUrl = "https://api.airtable.com/v0/appL5PANPfvJ59eji/Links?maxRecords=3&view=Grid%20view&fields%5B%5D=hash&maxRecords=100"
    headers = {
        "Authorization" : "Bearer " + app.config['AIRTABLE_KEY'],
    }
    
    createdHashes = []
    createdIds = []
    offset = ""

    while True:
        if offset == "":
            y = requests.get(listUrl, headers=headers)
        else:
            y = requests.get(listUrl, headers=headers, json={"offset":offset})

        for element in y.json()['records']:
            createdIds.append(element['id'])
            createdHashes.append(element['fields']['hash'])

        if "offset" in y.json():
            offset = y.json()['offset']
        else:
            break

    url = "https://api.airtable.com/v0/appL5PANPfvJ59eji/Links"

    fields = {
        "records" : [
            {
                "fields" : {
                    "hash" : hash_,
                    "text" : text,
                }
            }
        ]
    }

    if explode != "none":
        fields['records'][0]['fields']['exploding'] = True
        fields['records'][0]['fields']['exploding-field'] = explode
        fields['records'][0]['fields']['exploding-time'] = None
        if explode_input != "none":
            fields['records'][0]['fields']['exploding-time'] = int(explode_input)
    else:
        fields['records'][0]['fields']['exploding'] = False
        fields['records'][0]['fields']['exploding-field'] = None
        fields['records'][0]['fields']['exploding-time'] = None

    if hash_ in createdHashes:
        fields['records'][0]['id'] = createdIds[createdHashes.index(hash_)]
        x = requests.patch(url, json=fields, headers=headers)
    else:
        x = requests.post(url, json=fields, headers=headers)

    print('content uploaded with status code ' + str(x.status_code))
    return x.status_code

def getDataByRecordHash(hash_):
    listUrl = "https://api.airtable.com/v0/appL5PANPfvJ59eji/Links?maxRecords=3&view=Grid%20view&maxRecords=100"
    headers = {
        "Authorization" : "Bearer " + app.config['AIRTABLE_KEY'],
    }
    
    recordData = {}
    offset = ""

    while True:
        if offset == "":
            y = requests.get(listUrl, headers=headers)
        else:
            y = requests.get(listUrl, headers=headers, json={"offset":offset})

        for element in y.json()['records']:
            recordData[element['fields']['hash']] = element['fields']
            recordData[element['fields']['hash']]['id'] = element['id']

        if "offset" in y.json():
            offset = y.json()['offset']
        else:
            break
    
    if hash_ not in recordData.keys():
        print('hash not found -- invalid code')
        return -1, None
    else:
        print('hash found, record ID ' + recordData[hash_]['id'])
        return 1, recordData[hash_]

@app.route("/<code>", methods=['POST', 'GET'])
def link(code):

    if request.method == "GET":
        status, data = getDataByRecordHash(code)
        if status == -1:
            abort(404)
        
        md_template_string = markdown.markdown(data['text'], extensions=['fenced_code', 'codehilite'])
        marked_up = Markup(md_template_string)
        
        if "exploding" in data:
            if "exploding-time" in data:
                session['record_id'] = data['id']
                return render_template('pages/placeholder.view.html', renderText=marked_up, exploding=True, exploding_field=data['exploding-field'], exploding_time=data['exploding-time'])
            else:

                if data['exploding-field'] == 'firstview':
                    deleteRecord(data['id'])
                elif data['exploding-field'] == '30sec':
                    dateObj = datetime.now() + timedelta(seconds=30)
                    job = scheduler.add_job(func=deleteRecord, run_date=dateObj, args=[data['id']])

                session['record_id'] = data['id']
                return render_template('pages/placeholder.view.html', renderText=marked_up, exploding=True, exploding_field=data['exploding-field'])
        else:
            return render_template('pages/placeholder.view.html', renderText=marked_up, exploding=False)
    else:
        record_id = session.get('record_id')
        session.pop('record_id', None)
        if record_id is not None or record_id != "":
            deleteRecord(record_id)
        abort(404)

@app.route("/error", methods=['POST', 'GET'])
def error():
    return render_template('errors/placeholder.error.html', error_text="Something went wrong. Try again!")


@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == 'GET':
        return render_template('pages/placeholder.home.html', trigger_modal=False)
    elif request.method == 'POST':
        text = request.form['textarea-note']
        explode = request.form['does-it-explode']
        explode_input = request.form['does-it-explode-input']
        
        hashed = hashlib.md5(text.encode()).hexdigest()[:10]
        code = uploadText(hashed, text, explode, explode_input)

        if code == 200:
            return render_template('pages/placeholder.home.html', trigger_modal=True, hash_=hashed, original_text=text.strip())
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
    port = app.config['PORT']
    host = app.config['HOST']
    app.run(host=host, port=port)

