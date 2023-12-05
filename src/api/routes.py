"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Patient, Echo
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


#### Patients Modul ####

#query all patients
@api.route('/query/patients', methods=['GET'])
def get_patients():
    patients= Patient.query.all()
    serialized_patient= [patient.serialize() for patient in patients]
    return jsonify(serialized_patient),200


#query patient by id_card
@api.route('/query/patient/idcard/<int:id_card>', methods=['GET'])
def get_paient_by_id_card(id_card):
    current_patient= Patient.query.get(id_card)
    if not current_patient:
        return jsonify({"error": "patient not found"}), 404
    return jsonify(current_patient.serialize()),200


#create patients
@api.route('/create/patients', methods=['POST'])
def create_patients():
    data= request.get_json()
    name= data.get("name", None)
    id_card= data.get("id_card", None)
    phone= data.get("phone", None)
    age=  data.get("age", None)
    address= data.get("address", None)

    
    try:
        new_patient= Patient(name=name, id_card=id_card, phone=phone, age=age, address=address)
        db.session.add(new_patient)
        db.session.commit()
        return jsonify(new_patient.serialize()), 201

    except Exception as error:
        db.session.rollback()
        return jsonify(error.args), 500


# PUT patient
@api.route('/update/patient/<int:id>', methods=['PUT'])
def update_patient_by_id(id):
    data= request.get_json()
    name= data.get("name", None)
    id_card= data.get("id_card", None)
    phone= data.get("phone", None)
    age=  data.get("age", None)
    address= data.get("address", None)

    update_patient = Patient.query.get(id)
    if not update_patient:
        return jsonify({"error": "patient not found"}), 404

    try:
        update_patient.name = name
        update_patient.id_card = id_card
        update_patient.phone = phone
        update_patient.age = age
        update_patient.address = address
        db.session.commit()
        return jsonify({"patient": update_patient.serialize()}), 200

    except Exception as error:
        db.session.rollback()
        return error, 500
    

# delete a club
@api.route('/delete/patient/<int:id>', methods=['DELETE'])
def delete_patient_by_id(id):
    patient_to_delete = Patient.query.get(id)

    if not patient_to_delete:
        return jsonify({"error": "patient not found"}), 404

    try:
        db.session.delete(patient_to_delete)
        db.session.commit()
        return jsonify("patient deleted successfully"), 200

    except Exception as error:
        db.session.rollback()
        return error, 500



