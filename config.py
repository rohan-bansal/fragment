import os


# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management
SECRET_KEY = 'GbNYEqLb5IimxcfsRFNvb6MTC30Wmd1J'

# get airtable api key
AIRTABLE_KEY = os.environ.get("AIRTABLE_API_KEY")
BASE_URL = "https://api.airtable.com/v0/appL5PANPfvJ59eji/Links"

PORT = 5000
HOST = "0.0.0.0"
