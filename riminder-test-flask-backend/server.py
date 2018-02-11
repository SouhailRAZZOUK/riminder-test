"""Python Flask API Auth0 integration example
"""

from functools import wraps
import json
import bson
from bson.json_util import dumps, loads
from os import environ as env
#  Commented this package as I switched to requests package instead
# from six.moves.urllib.request import urlopen
import requests
from flask_pymongo import PyMongo

from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, jsonify, _request_ctx_stack
from flask_cors import cross_origin
from jose import jwt

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
AUTH0_DOMAIN = env.get("AUTH0_DOMAIN")
AUTH0_AUDIENCE = env.get("AUTH0_AUDIENCE")
ALGORITHMS = ["RS256"]
APP = Flask(__name__)

APP.config["MONGO_DBNAME"] = "Bookt-DB"
# APP.secret_key = 'm\xfc\x9aT\x05\x07b\xfd{@\x93\xb3M@"\xc5\xa6)\xa0\xdf\x8b\x81\xf7\xe3'

MONGO = PyMongo(APP)

# Format error response and append status code.


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@APP.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


def get_token_auth_header():
    """Obtains the access token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                         "description":
                         "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                         "description":
                         "Authorization header must start with"
                         " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description":
                         "Authorization header must be"
                         " Bearer token"}, 401)

    token = parts[1]
    return token


def requires_scope(required_scope):
    """Determines if the required scope is present in the access token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
        token_scopes = unverified_claims["scope"].split()
        for token_scope in token_scopes:
            if token_scope == required_scope:
                return True
    return False


def requires_auth(f):
    """Determines if the access token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()

        # Commented the next two lines because they are causing data type related errors
        # jsonurl = urlopen("https://souhail.auth0.com/.well-known/jwks.json")
        # jwks = json.loads(jsonurl.read())

        # The previous two lines were replace by the next two one, in order to load the json file as usual
        jsonurl_requests = requests.get(
            "https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = jsonurl_requests.json()
        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt.JWTError:
            raise AuthError({"code": "invalid_header",
                             "description":
                             "Invalid header. "
                             "Use an RS256 signed JWT Access Token"}, 401)
        if unverified_header["alg"] == "HS256":
            raise AuthError({"code": "invalid_header",
                             "description":
                             "Invalid header. "
                             "Use an RS256 signed JWT Access Token"}, 401)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=AUTH0_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
                # The next lines commented out as they are causing the mis-interpretation of the payload
                #,
                #    issuer=AUTH0_DOMAIN
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                 "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                 "description":
                                 "incorrect claims,"
                                 " please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                 "description":
                                 "Unable to parse authentication"
                                 " token."}, 400)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                         "description": "Unable to find appropriate key"}, 400)
    return decorated


# Controllers API
@APP.route("/api/public")
@cross_origin(headers=["Content-Type", "Authorization"])
def public():
    """No access token required to access this route
    """
    response = "All good. You don't need to be authenticated to call this"
    inserted_doc = MONGO.db.Pages.insert_one({'x': 1})
    return jsonify(message=response)


@APP.route("/api/test/<id>")
@cross_origin(headers=["Content-Type", "Authorization"])
def test(id):
    """No access token required to access this route
    """
    response = "All good. You don't need to be authenticated to call this"
    inserted_doc = MONGO.db.Pages.find_one({'_id': bson.objectid.ObjectId(id)})
    document = dumps(inserted_doc)
    return jsonify(doc=document)


@APP.route("/api/pages/<user>", methods=['GET'])
@cross_origin(headers=["Content-Type", "Authorization"])
def pages(user):
    all_pages_inserted = MONGO.db.Page.find({"_user": user})
    all_pages = dumps(all_pages_inserted)
    return jsonify(pages=all_pages)


@APP.route("/api/page/add", methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
def page_add():
    # try:
    page_to_insert = request.get_json()

    page_insert_result = MONGO.db.Page.insert_one({
        'title': page_to_insert['title'],
        "url": page_to_insert["url"],
        "description": page_to_insert["description"],
        "keywords": page_to_insert["keywords"],
        "_user": page_to_insert["_user"]
    })

    page_inserted = MONGO.db.Page.find_one({
        '_id': bson.objectid.ObjectId(page_insert_result.inserted_id)
    })

    page = dumps(page_inserted)

    return jsonify(page=page)

    # except KeyError:
    #     return jsonify(error="Invalid Data")


@APP.route("/api/page/<id>", methods=["GET", "DELETE"])
@cross_origin(headers=["Content-Type", "Authorization"])
def page(id):
    if request.method == "GET":
        page_inserted = MONGO.db.Page.find_one({'_id': bson.objectid.ObjectId(id)})
        page = dumps(page_inserted)
        return jsonify(page=page)
    elif request.method == "DELETE":
        page_deleted = MONGO.db.Page.delete_one({'_id': bson.objectid.ObjectId(id)})
        # page = dumps(page_deleted)
        return jsonify(count=page_deleted.deleted_count)



@APP.route("/api/private")
@cross_origin(headers=["Content-Type", "Authorization"])
@cross_origin(headers=["Access-Control-Allow-Origin", "*"])
@requires_auth
def private():
    """A valid access token is required to access this route
    """
    response = "All good. You only get this message if you're authenticated"
    return jsonify(message=response)


@APP.route("/api/user")
@cross_origin(headers=["Content-Type", "Authorization"])
@cross_origin(headers=["Access-Control-Allow-Origin", "*"])
@requires_auth
def user():
    """A valid access token is required to access this route
    """
    if requires_scope("profile"):
        token = get_token_auth_header()
        profile_headers = {"Authorization": "Bearer " + token}
        profile_response = requests.get(
            "https://souhail.auth0.com/userinfo", headers=profile_headers)
        profile = profile_response.json()
        return jsonify(profile=profile)
    raise AuthError({
        "code": "Anauthorized",
        "desciption": "You don't have access to this resource"
    }, 403)


@APP.route("/api/private-scoped")
@cross_origin(headers=["Content-Type", "Authorization"])
@cross_origin(headers=["Access-Control-Allow-Origin", "*"])
@requires_auth
def private_scoped():
    """A valid access token and an appropriate scope are required to access this route
    """
    if requires_scope("read:messages"):
        response = "All good. You're authenticated and the access token has the appropriate scope"
        return jsonify(message=response)
    raise AuthError({
        "code": "Anauthorized",
        "desciption": "You don't have access to this resource"
    }, 403)


if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=env.get("PORT", 3010))
