from app import app
from flask import (
    Flask,
    render_template,
    request,
    Response,
    flash,
    redirect,
    url_for,
    jsonify,
)
from models import Genre
from schemas import GenreSchema
from config.database import db
from decorators import parse_with
from sqlalchemy import exc


@app.route("/api/genre", methods=["GET"])
def get_genre():
    genres = Genre.query.all()

    return jsonify(count=len(genres), data=GenreSchema(many=True).dump(genres))


@app.route("/api/genre", methods=["POST"])
@parse_with(GenreSchema)
def create_genres(entity):
    genre = Genre(**entity)

    try:
        db.session.add(genre)
        db.session.commit()
        db.session.refresh(genre)
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(error=True, message="This record already exists"), 409
    except exc.SQLAlchemyError as err:
        app.logger.info(err)
        return jsonify(error=True, message="Server error"), 400

    return jsonify(message="Genre created successfully", data=GenreSchema().dump(genre))


@app.route("/api/genre/<int:id>", methods=["PUT"])
@parse_with(GenreSchema)
def update_genre(entity, id):
    genre = Genre.query.get(id)
    if not genre:
        return jsonify(message="Genre not found with id {}".format(id),), 404

    genre.name = entity["name"]

    try:
        db.session.add(genre)
        db.session.commit()
        db.session.refresh(genre)
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(error=True, message="This record already exists"), 409
    except exc.SQLAlchemyError as err:
        app.logger.info(err)
        return jsonify(error=True, message="Server error"), 400
    return jsonify(message="Genre updated successfully", data=GenreSchema().dump(genre))


@app.route("/api/genre/<int:id>", methods=["DELETE"])
def delete_genre(id):
    genre = Genre.query.get(id)
    if not genre:
        return jsonify(message="Genre not found with id {}".format(id),), 404

    db.session.delete(genre)
    db.session.commit()

    return jsonify(message="Genre deleted successfully",), 202
