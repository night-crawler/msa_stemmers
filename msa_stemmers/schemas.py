from marshmallow import Schema, fields


class LanguageSchema(Schema):
    alpha_2 = fields.Str()
    alpha_3 = fields.Str()
    name = fields.Str()
    scope = fields.Str()
    type = fields.Str()

