from marshmallow import Schema, fields, validate

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)

    title = fields.Str(
        required=True,
        validate=validate.Length(min=1)
    )

    description = fields.Str(
        required=True,
        validate=validate.Length(min=1)
    )

    completed = fields.Boolean(
        load_default=False,
        truthy={True},
        falsy={False}
    )

