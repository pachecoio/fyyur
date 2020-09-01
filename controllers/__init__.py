from app import app
from flask import render_template
from controllers.venue_controller import get_recent_venues
from controllers.artist_controller import get_recent_artists
from schemas import VenueSchema, ArtistSchema


@app.route("/")
def index():
    venues = get_recent_venues()
    artists = get_recent_artists()
    return render_template(
        "pages/home.html",
        venues=VenueSchema(many=True).dump(venues),
        artists=ArtistSchema(many=True).dump(artists)
    )


@app.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500
