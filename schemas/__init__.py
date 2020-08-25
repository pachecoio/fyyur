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


class VenueSchema(BaseSchema):
    seeking_talent = fields.Boolean()


class VenueCreateSchema(BaseSchema):
    name = fields.String(required=True)
    city = fields.String(required=True)
    state = fields.String(required=True)
    address = fields.String(required=True)
    phone = fields.String(required=True)
    genres = fields.Method('build_genres', deserialize='load_genres')
    city = fields.String(required=True)

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
