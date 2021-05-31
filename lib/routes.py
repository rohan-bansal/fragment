from flask import Flask, render_template, request, url_for, redirect, abort, send_from_directory, session
from flask import Blueprint
import bleach
from bleach_allowlist import print_tags, print_attrs, all_styles
import markdown.extensions.fenced_code
from markupsafe import Markup
from datetime import datetime, timedelta
import hashlib

from lib.airtable import *
from lib.background_scheduler import Schedule

fragment = Blueprint('fragment', __name__)
allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                'h1', 'h2', 'h3', 'p', 'img', 'div', 'p', 'br', 'span', 'hr']

allowed_attrs = {'*': ['class'],
                'a': ['href', 'rel'],
                'img': ['src', 'alt']}

@fragment.route("/content/viewcounter", methods=['POST'])
def viewcounter():
    ip_address = request.get_json()
    print(ip_address['ip'], request.base_url)

    record_hash = request.referrer.split('/')[-1].split("?")[0].split("#")[0]
    status, data = getDataByRecordHash(record_hash)
    if status == -1:
        abort(500)

    counter = data['view-counter']
    limit = data['variable-limit']
    addresses = ""

    if 'view-counter-addresses' in data:
        addresses = data['view-counter-addresses']

        if ip_address['ip'] not in addresses:
            addresses += "," + ip_address['ip']
            counter += 1
    else:
        addresses = ip_address['ip']
        counter += 1

    
    if counter >= limit:
        Schedule.instance().add_job(func=deleteRecord, run_date=(datetime.now() + timedelta(seconds=7)), args=[data['id']])
    else:
        updateRecordField(data['id'], {
            "view-counter-addresses":addresses,
            "view-counter":counter
        })

    return "success"

@fragment.route("/content/delete", methods=['POST'])
def delfunc():

    passphrase = request.form['passphrase']
    passphrase = passphrase.strip()

    record_hash = request.referrer.split('/')[-1].split("?")[0].split("#")[0]

    if passphrase is None or passphrase == "":
        return redirect(url_for('fragment.link', code=record_hash))

    status, data = getDataByRecordHash(record_hash)
    if status == -1:
        abort(500)

    if data['passphrase'] == passphrase:

        deleteRecord(data['id'])
        Schedule.instance().remove_job(data['id'])

        session['deleted_validation'] = "done"
        return redirect(url_for('fragment.delsuccess'))
    else:
        return redirect(url_for('fragment.link', code=record_hash))


@fragment.route("/content/delete_success", methods=['GET'])
def delsuccess():

    if session.get('deleted_validation') is None or session.get('deleted_validation') == "":
        abort(404)

    session.pop('deleted_validation', None)
    return render_template('pages/placeholder.delete_success.html')
    

@fragment.route("/<code>", methods=['POST', 'GET'])
def link(code):

    if request.method == "GET":
        status, data = getDataByRecordHash(code)
        if status == -1:
            abort(404)
        
        md_template_string = markdown.markdown(data['text'], extensions=['fenced_code', 'codehilite'], safe_mode=True, enable_attributes=False)
        marked_up = Markup(md_template_string)

        cleaned_mdx = bleach.clean(marked_up, strip=True, tags=print_tags, attributes=print_attrs, styles=all_styles).strip()
        
        if "exploding" in data:
            if "variable-limit" in data:
                session['record_id'] = data['id']

                dateObj = datetime.now()
                exploding_time = None
                exploding_date = None
                exploding_views = None

                if data['exploding-field'] == 'xhour':
                    createdTime = datetime.fromisoformat(data['created'].split("Z")[0])
                    dateObj = createdTime + timedelta(hours=data['variable-limit'])
                    exploding_time = dateObj.isoformat() + "Z"
                elif data['exploding-field'] == 'xsec':
                    dateObj = datetime.now() + timedelta(seconds=data['variable-limit'])
                    if not Schedule.instance().jobWithIdExists(data['id']):
                        job = Schedule.instance().add_job(func=deleteRecord, run_date=dateObj, id=data['id'], args=[data['id']])
                    exploding_time = data['variable-limit']
                elif data['exploding-field'] == 'xviews':
                    exploding_views = int(data['variable-limit'])

                return render_template(
                    'pages/placeholder.view.html', 
                    renderText=cleaned_mdx, 
                    exploding=True, 
                    exploding_field=data['exploding-field'], 
                    exploding_time=exploding_time,
                    exploding_date=exploding_date,
                    exploding_views=exploding_views
                )
               
            else:
                if data['exploding-field'] == 'firstview':
                    deleteRecord(data['id'])
                elif data['exploding-field'] == '30sec':
                    if not Schedule.instance().jobWithIdExists(data['id']):
                        dateObj = datetime.now() + timedelta(seconds=30)
                        job = Schedule.instance().add_job(func=deleteRecord, run_date=dateObj, id=data['id'], args=[data['id']])

                session['record_id'] = data['id']
                return render_template('pages/placeholder.view.html', renderText=cleaned_mdx, exploding=True, exploding_field=data['exploding-field'])
        else:
            return render_template('pages/placeholder.view.html', renderText=cleaned_mdx, exploding=False)
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
        code, passphrase, record_id = uploadText(hashed, text, explode, explode_input)

        if explode == 'xhour':
            if not Schedule.instance().jobWithIdExists(record_id):
                dateObj = datetime.now() + timedelta(hours=int(explode_input))
                job = Schedule.instance().add_job(func=deleteRecord, run_date=dateObj, id=record_id, args=[record_id])

        if code == 200:
            return render_template('pages/placeholder.home.html', trigger_modal=True, hash_=hashed, passphrase=passphrase, original_text=text.strip())
        else:
            return redirect(url_for('error'))

@fragment.errorhandler(500)
def internal_error(error):
    render_template('errors/placeholder.error.html', error_text="Internal Server Error (500)")


@fragment.errorhandler(404)
def not_found_error(error):
    return render_template('errors/placeholder.error.html', error_text="Invalid URL (404).")
