from app import app
from flask_marshmallow import Marshmallow
from marshmallow import fields

ma = Marshmallow(app)


class GenreSchema(ma.Schema):
    id = fields.Integer()
    name = fields.Str(required=True)
    label = fields.Str(required=True)


class BaseCreateSchema(ma.Schema):
    name = fields.String(required=True)
    city = fields.String(required=True)
    state = fields.String(required=True)
    address = fields.String(required=True)
    phone = fields.String(required=True)
    genres = fields.Method('build_genres', deserialize='load_genres')
    city = fields.String(required=True)
    facebook_link = fields.String()
    image_link = fields.String()
    website = fields.String()
    seeking_description = fields.String()

    def build_genres(self, obj):
        return obj.genres

    def load_genres(self, value):
        if isinstance(value, list):
            return value
        return [value]


class VenueShowSchema(ma.Schema):
    id = fields.Integer()
    artist_name = fields.Method('build_artist_name')
    artist_image_link = fields.Method('build_artist_image_link')
    start_time = fields.DateTime()

    def build_artist_name(self, obj):
        return obj.artist.name

    def build_artist_image_link(self, obj):
        return obj.artist.image_link

class BaseSchema(ma.Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    city = fields.String(required=True)
    state = fields.String(required=True)
    address = fields.String(required=True)
    phone = fields.String(required=True)
    genres = fields.Method('build_genres')
    website = fields.String()
    facebook_link = fields.String(required=True)
    seeking_description = fields.String()
    image_link = fields.String()
    past_shows = fields.List(
        fields.Nested(VenueShowSchema),
    )
    upcoming_shows = fields.List(
        fields.Nested(VenueShowSchema),
    )

    def build_genres(self, obj):
        return [
            genre.name for genre in obj.genres
        ]


class VenueSchema(BaseSchema):
    seeking_talent = fields.Boolean()


class VenueCreateSchema(BaseCreateSchema):
    seeking_talent = fields.Boolean()


class VenueEditSchema(BaseCreateSchema):
    name = fields.String()
    city = fields.String()
    state = fields.String()
    address = fields.String()
    phone = fields.String()
    city = fields.String()
    seeking_talent = fields.Boolean()


class ArtistSchema(BaseSchema):
    seeking_venue = fields.Boolean()


class ArtistListSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String()


class ArtistCreateSchema(BaseCreateSchema):
    seeking_venue = fields.Boolean()

class ArtistEditSchema(BaseCreateSchema):
    name = fields.String()
    city = fields.String()
    state = fields.String()
    address = fields.String()
    phone = fields.String()
    city = fields.String()
    seeking_venue = fields.Boolean()


class ShowListSchema(ma.Schema):
    id = fields.Integer()
    start_time = fields.DateTime()
    artist = fields.Nested(ArtistSchema)
    artist_id = fields.Function(
        lambda e: e.artist.id
    )
    artist_name = fields.Function(
        lambda e: e.artist.name
    )
    artist_image_link = fields.Function(
        lambda e: e.artist.image_link
    )
    venue = fields.Nested(VenueSchema)
    venue_id = fields.Function(
        lambda e: e.venue.id
    )
    venue_name = fields.Function(
        lambda e: e.venue.name
    )

class ShowCreateSchema(ma.Schema):
    artist_id = fields.Integer()
    venue_id = fields.Integer()
    start_time = fields.DateTime()
