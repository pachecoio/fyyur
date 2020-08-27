from app import app
from flask_marshmallow import Marshmallow
from marshmallow import fields

ma = Marshmallow(app)


class GenreSchema(ma.Schema):
    id = fields.Integer()
    name = fields.Str(required=True)
    label = fields.Str(required=True)


class BaseSchema(ma.Schema):
    id = fields.Integer()
    name = fields.Str()
    city = fields.Str()
    state = fields.Str()
    phone = fields.Str()
    genres = fields.Str()
    image_link = fields.Str()
    facebook_link = fields.Str()
    website = fields.Str()
    genres = fields.List(fields.Nested(GenreSchema))


class VenueShowSchema(ma.Schema):
    id = fields.Integer()
    artist_name = fields.Method('build_artist_name')
    artist_image_link = fields.Method('build_artist_image_link')
    start_time = fields.DateTime()

    def build_artist_name(self, obj):
        return obj.artist.name

    def build_artist_image_link(self, obj):
        return obj.artist.image_link

class VenueSchema(BaseSchema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    city = fields.String(required=True)
    state = fields.String(required=True)
    address = fields.String(required=True)
    phone = fields.String(required=True)
    genres = fields.Method('build_genres')
    website = fields.String()
    facebook_link = fields.String(required=True)
    seeking_talent = fields.Boolean()
    seeking_description = fields.String()
    image_link = fields.String()
    past_shows = fields.List(
        fields.Nested(VenueShowSchema),
        attribute="shows"
    )
    # upcoming_shows = past_shows = fields.List(
    #     fields.Nested(VenueShowSchema),
    #     attribute="shows"
    # )

    def build_genres(self, obj):
        return [
            genre.name for genre in obj.genres
        ]


class VenueCreateSchema(BaseSchema):
    name = fields.String(required=True)
    city = fields.String(required=True)
    state = fields.String(required=True)
    address = fields.String(required=True)
    phone = fields.String(required=True)
    genres = fields.Method('build_genres', deserialize='load_genres')
    city = fields.String(required=True)
    facebook_link = fields.String()
    website = fields.String()
    seeking_description = fields.String()
    seeking_talent = fields.Boolean()

    def build_genres(self, obj):
        return obj.genres

    def load_genres(self, value):
        if isinstance(value, list):
            return value
        return [value]


class ArtistSchema(BaseSchema):
    seeking_venue = fields.Boolean()


class ShowSchema(ma.Schema):
    id = fields.Integer()
    start_time = fields.DateTime()
    artist = fields.Nested(ArtistSchema)
    venue = fields.Nested(VenueSchema)
