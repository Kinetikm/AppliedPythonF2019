from marshmallow import Schema, fields, validate, validates_schema
from auth_service.utils.exception import ApiException


class SignupSchema(Schema):
    email = fields.Str(required=True, validate=validate.Regexp(r'^[A-Za-z]{1,15}@[a-z]{1,7}\.[a-z]{2,5}$'))
    login = fields.Str(required=True, validate=validate.Length(max=10))
    password = fields.Str(required=True, validate=validate.Length(min=5))
    re_password = fields.Str(required=True, validate=validate.Length(min=5))

    @validates_schema
    def validate_time(self, data, **kwargs):
        if data["password"] != data["re_password"]:
            raise ApiException(400, "Data incorrect", "Repassword dont the same")

    def handle_error(self, exc, data, **kwargs):
        raise ApiException(400, "Data incorrect", exc.messages)


class AuthSchema(Schema):
    login = fields.Str(required=True, validate=validate.Length(max=10))
    password = fields.Str(required=True, validate=validate.Length(min=5))

    def handle_error(self, exc, data, **kwargs):
        raise ApiException(400, "Data incorrect", exc.messages)
