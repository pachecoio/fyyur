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
from models import Venue, Artist, Genre, Show
from forms import build_artist_form
from schemas import ArtistListSchema, ArtistCreateSchema, ArtistSchema, ArtistEditSchema
from decorators import parse_with
from sqlalchemy import exc, func, or_
from config.database import db
import datetime
from enum import Enum
from models import WeekDays

#  Artists
#  ----------------------------------------------------------------
@app.route("/artists")
def artists():
    artists = Artist.query.all()
    data = ArtistListSchema(many=True).dump(artists)
    return render_template("pages/artists.html", artists=data)


@app.route("/artists/search", methods=["POST"])
def search_artists():
    search_term = request.form.get("search_term", "")
    artists = (
        db.session.query(
            Artist.id, Artist.name, func.count(Show.id).label("num_upcoming_shows")
        )
        .select_from(Artist)
        .outerjoin(Show, Show.artist_id == Artist.id)
        .filter(
            or_(
                Artist.name.ilike("%{}%".format(search_term)),
                Artist.city.ilike("%{}%".format(search_term)),
                Artist.state.ilike("%{}%".format(search_term)),
            )
        )
        .group_by(Artist.id)
        .all()
    )
    response = {
        "count": len(artists),
        "data": artists,
    }
    return render_template(
        "pages/search_artists.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


@app.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    shows = artist.shows
    artist.past_shows = filter(
        lambda show: show.start_time <= datetime.datetime.now(), shows
    )
    artist.upcoming_shows = filter(
        lambda show: show.start_time > datetime.datetime.now(), shows
    )
    return render_template("pages/show_artist.html", artist=ArtistSchema().dump(artist))


#  Update
#  ----------------------------------------------------------------
@app.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    genre_list = Genre.query.all()
    genres = [(genre.name, genre.label) for genre in genre_list]
    form = build_artist_form(genres)
    artist = Artist.query.get(artist_id)
    return render_template(
        "forms/edit_artist.html", form=form, artist=ArtistSchema().dump(artist)
    )


@app.route("/artists/<int:artist_id>/edit", methods=["POST"])
@parse_with(ArtistEditSchema)
def edit_artist_submission(entity, artist_id):
    genres = Genre.query.filter(Genre.name.in_(entity["genres"])).all()
    artist = Artist.query.get(artist_id)
    for key, value in entity.items():
        if key == "genres":
            artist.genres = genres
        else:
            setattr(artist, key, value)
    try:
        db.session.add(artist)
        db.session.commit()
        db.session.refresh(artist)
        flash("artist " + artist.name + " was successfully listed!")
    except exc.SQLAlchemyError as err:
        db.session.rollback()
        app.logger.info(err)
        flash("An error occurred. artist " + artist.name + " could not be listed.")
    return redirect(url_for("show_artist", artist_id=artist_id))


@app.route("/artists/<artist_id>", methods=["DELETE"])
def delete_artist(artist_id):
    artist = Artist.query.get(artist_id)

    if not artist:
        return jsonify(message="artist not found with id".format(artist_id),), 404
    try:
        db.session.delete(artist)
        db.session.commit()
        return (
            jsonify(message="artist {} delete successfully".format(artist.name),),
            202,
        )
    except exc.SQLAlchemyError as err:
        db.session.rollback()
        app.logger.info(err)
        return jsonify(message="Error deleting artist {}".format(artist.name),), 400


#  Create Artist
#  ----------------------------------------------------------------


@app.route("/artists/create", methods=["GET"])
def create_artist_form():
    genre_list = Genre.query.all()
    genres = [(genre.name, genre.label) for genre in genre_list]
    form = build_artist_form(genres)
    return render_template("forms/new_artist.html", form=form)


@app.route("/artists/create", methods=["POST"])
@parse_with(ArtistCreateSchema)
def create_artist_submission(entity):
    genres = Genre.query.filter(Genre.name.in_(entity["genres"])).all()
    del entity["genres"]
    artist = Artist(**entity, genres=genres,)
    try:
        db.session.add(artist)
        db.session.commit()
        db.session.refresh(artist)
        flash("Artist " + artist.name + " was successfully listed!")
    except exc.IntegrityError:
        db.session.rollback()
        flash("There is already an artist with the name " + artist.name + ".")
    except exc.SQLAlchemyError as err:
        db.session.rollback()
        app.logger.info(err)
        flash("An error occurred. Artist " + artist.name + " could not be listed.")
    return render_template("pages/home.html")


def get_recent_artists(limit=10):
    return Artist.query.order_by(Artist.created_at.desc()).limit(limit)
