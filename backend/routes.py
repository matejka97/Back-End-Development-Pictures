from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """return array of pictures URLs"""
    try:
        if data:
            pic_urls = [pic["pic_url"] for pic in data if "pic_url" in pic]
            return jsonify(pic_urls), 200
        return jsonify([]), 200 # return empty list if missing data
    except Exception as e:
        return jsonify({"message": "Internal server error", 
                        "error": str(e)}), 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """returns URLs of specific picture accroding to its ID"""
    try:
        if data:
            picture = next((pic for pic in data
                             if "id" in pic.keys() and pic["id"]==id),None)
            if picture is None:
                return jsonify({"message": f"No Picutures with for {id}"}), 404
            else:
                return jsonify(picture), 200
        else:
            return jsonify({"message": "No Data Available"}), 204
    except Exception as e:
        return jsonify({"message": "Internal server error" ,
                        "error": str(e)}), 500


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """posts new picture into data"""
    new_picture = request.get_json()

    current_pictures_ids = [pic["id"] for pic in data]

    if new_picture["id"] in current_pictures_ids:
        return jsonify({"message": f"picture with id {new_picture["id"]} already present"}), 302
    

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pass

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    pass
