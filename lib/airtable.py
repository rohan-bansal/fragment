from config import AIRTABLE_BASE_URL, AIRTABLE_KEY
import requests, json
from datetime import datetime
from xkcdpass import xkcd_password as xp

wordfile = xp.locate_wordfile()
words = xp.generate_wordlist(wordfile=wordfile, min_length=4, max_length=9)

def deleteRecord(id_):
    deleteUrl = AIRTABLE_BASE_URL + "/" + id_
    headers = {
        "Authorization" : "Bearer " + AIRTABLE_KEY,
    }

    x = requests.delete(deleteUrl, headers=headers)
    print('record ID ' + id_ + ' deleted with status code ' + str(x.status_code))

    return x.status_code

def updateRecordField(id_, field_data):
    updateURL = AIRTABLE_BASE_URL + "/" + id_
    headers = {
        "Authorization" : "Bearer " + AIRTABLE_KEY,
        "Content-Type" : "application/json"
    }

    data = {
        "fields" : field_data
    }

    x = requests.patch(updateURL, headers=headers, json=data)
    print('record ID ' + id_ + ' patched with status code ' + str(x.status_code))

    return x.status_code

def uploadText(hash_, text, explode, explode_input):

    listUrl = AIRTABLE_BASE_URL + "?maxRecords=3&view=Grid%20view&fields%5B%5D=hash&maxRecords=100"
    headers = {
        "Authorization" : "Bearer " + AIRTABLE_KEY,
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

    securePass = xp.generate_xkcdpassword(words, numwords=5)

    fields = {
        "records" : [
            {
                "fields" : {
                    "hash" : hash_,
                    "text" : text,
                    "passphrase" : securePass,
                    "view-counter" : 0
                }
            }
        ]
    }

    if explode != "none":
        fields['records'][0]['fields']['exploding'] = True
        fields['records'][0]['fields']['exploding-field'] = explode
        fields['records'][0]['fields']['variable-limit'] = None
        if explode_input != "none":
            fields['records'][0]['fields']['variable-limit'] = int(explode_input)
    else:
        fields['records'][0]['fields']['exploding'] = False
        fields['records'][0]['fields']['exploding-field'] = None
        fields['records'][0]['fields']['variable-limit'] = None

    if hash_ in createdHashes:
        fields['records'][0]['id'] = createdIds[createdHashes.index(hash_)]
        x = requests.patch(AIRTABLE_BASE_URL, json=fields, headers=headers)
    else:
        x = requests.post(AIRTABLE_BASE_URL, json=fields, headers=headers)

    print('content uploaded with status code ' + str(x.status_code))
    print()
    return x.status_code, securePass, json.loads(x.content.decode("utf-8"))['records'][0]['id']

def getDataByRecordHash(hash_):
    listUrl = AIRTABLE_BASE_URL + "?maxRecords=3&view=Grid%20view&maxRecords=100"
    headers = {
        "Authorization" : "Bearer " + AIRTABLE_KEY,
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
        print(recordData[hash_]['created'])
        return 1, recordData[hash_]