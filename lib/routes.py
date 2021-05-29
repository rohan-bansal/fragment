from flask import Flask, render_template, request, url_for, redirect, abort, send_from_directory, session
from flask import Blueprint
import markdown.extensions.fenced_code
from markupsafe import Markup
from datetime import datetime, timedelta
import hashlib

from lib.airtable import *
from lib.background_scheduler import Schedule

fragment = Blueprint('fragment', __name__)


@fragment.route("/content/delete", methods=['POST'])
def delfunc():

    print(request.referrer)
    passphrase = request.form['passphrase']
    passphrase = passphrase.strip()
    print(passphrase)

@fragment.route("/<code>", methods=['POST', 'GET'])
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
                    job = Schedule.instance().add_job(func=deleteRecord, run_date=dateObj, args=[data['id']])

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

@fragment.route("/error", methods=['POST', 'GET'])
def error():
    return render_template('errors/placeholder.error.html', error_text="Something went wrong. Try again!")

@fragment.route('/', methods=["POST", "GET"])
def home():
    if request.method == 'GET':
        return render_template('pages/placeholder.home.html', trigger_modal=False)
    elif request.method == 'POST':
        text = request.form['textarea-note']
        explode = request.form['does-it-explode']
        explode_input = request.form['does-it-explode-input']
        
        hashed = hashlib.md5(text.encode()).hexdigest()[:10]
        code, passphrase = uploadText(hashed, text, explode, explode_input)

        if code == 200:
            return render_template('pages/placeholder.home.html', trigger_modal=True, hash_=hashed, passphrase=passphrase, original_text=text.strip())
        else:
            return redirect(url_for('error'))

@fragment.errorhandler(500)
def internal_error(error):
    render_template('errors/placeholder.error.html', error_text="Code 500.")


@fragment.errorhandler(404)
def not_found_error(error):
    return render_template('errors/placeholder.error.html', error_text="Invalid URL (404).")
