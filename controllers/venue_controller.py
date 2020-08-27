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
from models import Venue, Genre, Show
from forms import build_venue_form
from schemas import VenueCreateSchema, VenueSchema
from decorators import parse_with
from config.database import db
from sqlalchemy import exc, func

#  Venues
#  ----------------------------------------------------------------

DEFAULT_GENRES = [
    ("Alternative", "Alternative"),
    ("Blues", "Blues"),
    ("Classical", "Classical"),
    ("Country", "Country"),
    ("Electronic", "Electronic"),
    ("Folk", "Folk"),
    ("Funk", "Funk"),
    ("Hip-Hop", "Hip-Hop"),
    ("Heavy Metal", "Heavy Metal"),
    ("Instrumental", "Instrumental"),
    ("Jazz", "Jazz"),
    ("Musical Theatre", "Musical Theatre"),
    ("Pop", "Pop"),
    ("Punk", "Punk"),
    ("R&B", "R&B"),
    ("Reggae", "Reggae"),
    ("Rock n Roll", "Rock n Roll"),
    ("Soul", "Soul"),
    ("Other", "Other"),
]

@app.route("/venues")
def venues():
    venues = Venue.query.order_by(Venue.state).all()

    data = {}

    for venue in venues:
        key = "{}-{}".format(venue.state, venue.city)
        if key in data:
            data[key]["venues"].append(
                {"id": venue.id, "name": venue.name, "num_upcoming_shows": 0,}
            )
        else:
            data[key] = {
                "city": venue.city,
                "state": venue.state,
                "venues": [
                    {"id": venue.id, "name": venue.name, "num_upcoming_shows": 0,}
                ],
            }

    data = data.values()
    return render_template("pages/venues.html", areas=data)


@app.route("/venues/search", methods=["POST"])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get("search_term", "")
    print(search_term)
    venues = (
        db.session.query(
            Venue.id,
            Venue.name,
            func.count(Show.id).label("num_upcoming_shows")
        )
        .select_from(Venue)
        .outerjoin(
            Show, Show.venue == Venue.id
        )
        .filter(Venue.name.ilike("%{}%".format(search_term)))
        .group_by(Venue.id)
        .all()
    )
    response = {
        "count": len(venues),
        "data": venues,
    }
    return render_template(
        "pages/search_venues.html",
        results=response,
        search_term=search_term,
    )


@app.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    venue = Venue.query.get(venue_id)
    return render_template("pages/show_venue.html", venue=VenueSchema().dump(venue))


#  Create Venue
#  ----------------------------------------------------------------


@app.route("/venues/create", methods=["GET"])
def create_venue_form():
    genre_list = Genre.query.all()
    genres = [(genre.name, genre.label) for genre in genre_list]
    form = build_venue_form(genres)
    return render_template("forms/new_venue.html", form=form)


@app.route("/venues/create", methods=["POST"])
@parse_with(VenueCreateSchema)
def create_venue_submission(entity):

    genres = Genre.query.filter(Genre.name.in_(entity["genres"])).all()
    del entity["genres"]

    # TODO: insert form data as a new Venue record in the db, instead
    venue = Venue(**entity, genres=genres,)
    try:
        db.session.add(venue)
        db.session.commit()
        db.session.refresh(venue)
        flash("Venue " + venue.name + " was successfully listed!")
    except exc.IntegrityError:
        db.session.rollback()
        flash("There is already a venue with the name " + venue.name + ".")
    except exc.SQLAlchemyError as err:
        db.session.rollback()
        app.logger.info(err)
        flash("An error occurred. Venue " + venue.name + " could not be listed.")
    return render_template("pages/home.html")


@app.route("/venues/<venue_id>", methods=["DELETE"])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


@app.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    form = VenueForm()
    venue = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template("forms/edit_venue.html", form=form, venue=venue)


@app.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for("show_venue", venue_id=venue_id))

