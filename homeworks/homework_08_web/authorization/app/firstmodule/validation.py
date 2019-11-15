from marshmallow import Schema, fields, ValidationError


class RegistrtationSchema(Schema):
    email = fields.Str(required=True)
    login = fields.Str(required=True)
    passwd = fields.Str(required=True)
    confirm_passwd = fields.Str(required=True)

    class Meta:
        strict = True


def validate_passwd(json_request):
    if json_request['passwd'] != json_request['confirm_passwd']:
        raise ValidationError('Passwords do not match')
