from flask import Flask, send_from_directory, request

from lib.routes import fragment
from lib.background_scheduler import Schedule
from config import PORT, HOST


app = Flask(__name__, static_folder='static')
app.config.from_object('config')

app.register_blueprint(fragment)
Schedule.instance()

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

if __name__ == '__main__':
    port = PORT
    host = HOST
    app.run(host=host, port=port)