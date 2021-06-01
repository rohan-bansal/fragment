from config import SUPABASE_BASE_URL, SUPABASE_KEY
import requests, json
from datetime import datetime
from xkcdpass import xkcd_password as xp


def uploadText(hash_, text, explode, explode_input):

    listUrl = SUPABASE_BASE_URL + "?select=hash"
    headers = {
        "apikey" : SUPABASE_KEY,
        "Authorization" : "Bearer " + SUPABASE_KEY,
    }