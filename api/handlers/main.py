from flask import jsonify

from api import app


@app.route('/')
def index():
    """ Redirect from root to admin page """
    return app.send_static_file('client/home.html')


@app.route('/api/client/version', methods=['GET'])
def get_version():
    """
    Return a current server and API versions.
    """
    response = {
        "api_version": app.config["API_VERSION"],
        "server_version": 'dev',
        "build_date": app.config["BUILD_DATE"]
    }
    return jsonify(response)
