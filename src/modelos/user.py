from ..db import db
import os


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    imagen_id = db.relationship("Imagen")

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            #"imagen_id": self.imagen_id,
            #"image_ruta": Imagen.query.get(self.imagen_id).serialize()['ruta']
            # do not serialize the password, its a security breach
        }

    def serializeImagen(self):
        return {
            "id": self.id,
            "email": self.email,
            "imagen_id": self.imagen_id,
            "image_ruta": Imagen.query.get(self.imagen_id).serialize()['ruta']
            # do not serialize the password, its a security breach
        }