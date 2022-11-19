import os
from ..main import request, jsonify, app, bcrypt, create_access_token, get_jwt_identity, jwt_required, get_jwt
from ..db import db
from ..modelos import User, Imagen
from flask import Flask, url_for
from datetime import datetime, timezone, time
import json
from ..utils import APIException

@app.route('/subirImagen' , methods=['POST'])
@jwt_required()
def subirImagen():
    print("id del usuario:", get_jwt_identity()) #imprimiendo la identidad del usuario que es el id
    userID = get_jwt_identity()
    body = request.get_json()
    print(body)
    #print(body['username'])     
    try:
        if body is None:
            raise APIException("Body está vacío o email no viene en el body, es inválido" , status_code=400)
        if body['ruta'] is None or body['ruta']=="":
            raise APIException("email es inválido" , status_code=400)    

        new_image = Imagen(ruta=body['ruta'], user_id=userID)
       

        print(new_image)
        #print(new_user.serialize())
        db.session.add(new_image) 
        db.session.commit()
        return jsonify({"mensaje": "Imagen creada exitósamente"}), 201

    except Exception as err:
        db.session.rollback()
        print(err)
        return jsonify({"mensaje": "error al registrar imagen"}), 500

@app.route('/lista-imagenes', methods=['get'])
#@jwt_required()
def allImages():
    imagenes = Imagen.query.all() #Objeto de SQLAlchemy
    imagenes = list(map(lambda item: item.serialize(), imagenes))
    print("entré en endpoint")
    response_body={
        "lista": imagenes
    }
    return jsonify(response_body), 200