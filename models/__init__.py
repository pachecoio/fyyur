from config.database import db
# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

genre_venue = db.Table(
    "genre_venue",
    db.Column("genre_id", db.Integer, db.ForeignKey("Genre.id", ondelete="CASCADE"), primary_key=True),
    db.Column("venue_id", db.Integer, db.ForeignKey("Venue.id", ondelete="CASCADE"), primary_key=True),
)

genre_artist = db.Table(
    "genre_artist",
    db.Column("genre_id", db.Integer, db.ForeignKey("Genre.id", ondelete="CASCADE"), primary_key=True),
    db.Column("artist_id", db.Integer, db.ForeignKey("Artist.id", ondelete="CASCADE"), primary_key=True),
)


class Genre(db.Model):
    __tablename__ = "Genre"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    label = db.Column(db.String(), nullable=False, unique=True)


class Venue(db.Model):
    __tablename__ = "Venue"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    genres = db.relationship(
        "Genre", secondary=genre_venue, backref=db.backref("venues", lazy=True), cascade="all, delete"
    )
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship("Show")


class Artist(db.Model):
    __tablename__ = "Artist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    genres = db.relationship(
        "Genre", secondary=genre_artist, backref=db.backref("artists", lazy=True), cascade="all, delete"
    )
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship("Show")


class Show(db.Model):
    __tablename__ = "Show"

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    venue = db.Column(db.Integer, db.ForeignKey("Venue.id"))
    artist = db.Column(db.Integer, db.ForeignKey("Artist.id"))

