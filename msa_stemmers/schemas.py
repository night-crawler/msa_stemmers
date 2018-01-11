import builtins

from marshmallow import Schema, fields


class LanguageSchema(Schema):
    alpha_2 = fields.Str()
    alpha_3 = fields.Str()
    name = fields.Method('get_name')
    scope = fields.Str()
    type = fields.Str()

    @staticmethod
    def get_name(obj):
        if '_' in builtins.__dict__:
            return _(obj.name).capitalize()
        return obj.name.capitalize()
