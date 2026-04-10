from marshmallow import Schema, fields, validate, ValidationError
import re

class CategorySchema(Schema):
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50) # not sure how to enforce uniqueness
    )
    color = fields.Str(
        validate=validate.Regexp(
            r'^#[0-9a-fA-F]{6}$',
            error="Not a valid hex color code"
        )
    )

class CategoryResponseSchema(Schema):
    name=fields.Str()
    color=fields.Str()

class TaskSchema(Schema):

    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )
    description = fields.Str(
        validate=validate.Length(max=500)
    )
    due_date = fields.DateTime(format="iso")
    category_id = fields.Nested(CategorySchema)

class TaskResponseSchema(Schema):
    id=fields.Int(dump_only=True)
    title=fields.Str()
    description=fields.Str(allow_none=True)
    completed=fields.Boolean()
    due_date=fields.DateTime()
    category_id=fields.Int()
    created_at=fields.DateTime()
    updated_at=fields.DateTime()
