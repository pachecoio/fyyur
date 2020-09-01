from app import app
from flask import render_template, flash, request, jsonify
from forms import ShowForm
from models import Show, Artist, Venue
from schemas import ShowListSchema, ShowCreateSchema
from decorators import parse_with
from sqlalchemy import exc, func, or_
from config.database import db
#  Shows
#  ----------------------------------------------------------------


@app.route("/shows")
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    shows = Show.query.all()
    return render_template("pages/shows.html", shows=ShowListSchema(many=True).dump(shows))


@app.route("/shows/create")
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@app.route("/shows/create", methods=["POST"])
@parse_with(ShowCreateSchema)
def create_show_submission(entity):
    artist = Artist.query.get(entity["artist_id"])
    venue = Venue.query.get(entity["venue_id"])
    show = Show(
        artist_id=artist.id,
        venue_id=venue.id,
        start_time=entity["start_time"]
    )
    try:
        db.session.add(show)
        db.session.commit()
        db.session.refresh(show)
        flash("Show was successfully listed!")
    except exc.IntegrityError:
        db.session.rollback()
        flash("There is already a venue with the name " + venue.name + ".")
    except exc.SQLAlchemyError as err:
        db.session.rollback()
        app.logger.info(err)
        flash('An error occurred. Show could not be listed.')
    return render_template("pages/home.html")

@app.route("/shows/search", methods=["POST"])
def search_shows():
    search_term = request.form.get("search_term", "")
    print(search_term)
    shows = (
        Show.query
        .join(Artist, Show.artist_id == Artist.id)
        .join(Venue, Show.venue_id == Venue.id)
        .filter(
            or_(
                Venue.name.ilike("%{}%".format(search_term)),
                Artist.name.ilike("%{}%".format(search_term))
            )
        )
        .group_by(Show.id)
        .all()
    )
    response = {
        "count": len(shows),
        "data": ShowListSchema(many=True).dump(shows),
    }
    return render_template(
        "pages/show.html", results=response, search_term=search_term,
    )

@app.route("/shows/<show_id>", methods=["DELETE"])
def delete_show(show_id):
    show = Show.query.get(show_id)
    
    if not show:
        return jsonify(
            message="show not found with id".format(show_id),
        ), 404
    try:
        db.session.delete(show)
        db.session.commit()
        return jsonify(
            message="show {} delete successfully".format(show.id),
        ), 202
    except exc.SQLAlchemyError as err:
        db.session.rollback()
        app.logger.info(err)
        return jsonify(
            message="Error deleting show {}".format(show.id),
        ), 400