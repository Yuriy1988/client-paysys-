from api import app
from api.schemas.version import VersionSchema
from config import API_VERSION, BUILD_DATE
from flask import jsonify


@app.route('/api/client/version', methods=['GET'])
def get_version():
    """
    Return a current server and API versions.
    """
    responce = {
        "api_version": API_VERSION,
        "server_version": 'dev',
        "build_date": BUILD_DATE
    }
    version_schema = VersionSchema()
    result = version_schema.dump(responce)
    return jsonify(result.data)
