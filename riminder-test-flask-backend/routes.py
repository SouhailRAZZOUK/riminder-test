import json
from utils import *
from flask import jsonify

def public():
    """No access token required to access this route
    """
    response = "All good. You don't need to be authenticated to call this"
    inserted_doc = MONGO.db.test.insert_one({'x': 1})
    return jsonify(message=response)

def test(id):
    """No access token required to access this route
    """
    response = "All good. You don't need to be authenticated to call this"
    inserted_doc = MONGO.db.test.find_one({'_id': bson.objectid.ObjectId(id)})
    print(inserted_doc)
    document = dumps(inserted_doc)
    return jsonify(doc=document)


def private():
    """A valid access token is required to access this route
    """
    response = "All good. You only get this message if you're authenticated"
    return jsonify(message=response)

def user():
    """A valid access token is required to access this route
    """
    if requires_scope("profile"):
        token = get_token_auth_header()
        profile_headers = {"Authorization": "Bearer " + token}
        profile_response = requests.get("https://souhail.auth0.com/userinfo", headers=profile_headers)
        profile = profile_response.json()
        print(profile)
        return jsonify(profile=profile)
    raise AuthError({
        "code": "Anauthorized",
        "desciption": "You don't have access to this resource"
    }, 403)


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
