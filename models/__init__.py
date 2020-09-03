from config.database import db
import datetime
from enum import Enum

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


class WeekDays(Enum):
    Sunday = 0
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6

    @classmethod
    def choices(cls):
        return [(choice.value, str(choice).replace("WeekDays.", "")) for choice in cls]

    @classmethod
    def coerce(cls, item):
        return item if isinstance(item, WeekDays) else WeekDays[item]


genre_venue = db.Table(
    "genre_venue",
    db.Column("genre_id", db.Integer, db.ForeignKey("Genre.id"), primary_key=True),
    db.Column("venue_id", db.Integer, db.ForeignKey("Venue.id"), primary_key=True),
)

genre_artist = db.Table(
    "genre_artist",
    db.Column("genre_id", db.Integer, db.ForeignKey("Genre.id"), primary_key=True),
    db.Column("artist_id", db.Integer, db.ForeignKey("Artist.id"), primary_key=True),
)


class TimestampMixin(object):
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Genre(db.Model, TimestampMixin):
    __tablename__ = "Genre"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    label = db.Column(db.String(), nullable=False, unique=True)


class Venue(db.Model, TimestampMixin):
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
        "Genre", secondary=genre_venue, backref=db.backref("venues", lazy=True),
    )
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship("Show", backref=db.backref("venue", lazy=True), cascade="all, delete-orphan")


class Artist(db.Model, TimestampMixin):
    __tablename__ = "Artist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    genres = db.relationship(
        "Genre", secondary=genre_artist, backref=db.backref("artists", lazy=True),
    )
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship("Show", backref=db.backref("artist", lazy=True), cascade="all, delete-orphan")
    week_days_availability = db.Column(db.String())


class Show(db.Model, TimestampMixin):
    __tablename__ = "Show"

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id", ondelete="CASCADE"))
    artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id", ondelete="CASCADE"))
    duration = db.Column(db.Integer)

    

