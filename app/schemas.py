from marshmallow import Schema, fields, post_dump, validate

class CategorySchema(Schema):
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50)
    )
    color = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Regexp(
            r'^#[0-9a-fA-F]{6}$',
            error="Not a valid hex color code"
        )
    )

class CategoryResponseSchema(Schema):
    id = fields.Int()
    name=fields.Str()
    color=fields.Str(allow_none=True)
    task_count = fields.Int(required=False)
    tasks = fields.List(fields.Dict(), required=False)

class TaskSchema(Schema):
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )
    description = fields.Str(
        required=False,
        allow_none=True,
        validate=validate.Length(max=500)
    )
    completed = fields.Boolean(required=False)
    due_date = fields.DateTime(format="iso", required=False, allow_none=True)
    category_id = fields.Int(required=False, allow_none=True)


class TaskUpdateSchema(Schema):
    title = fields.Str(required=False, validate=validate.Length(min=1, max=100))
    description = fields.Str(required=False, allow_none=True, validate=validate.Length(max=500))
    completed = fields.Boolean(required=False)
    due_date = fields.DateTime(format="iso", required=False, allow_none=True)
    category_id = fields.Int(required=False, allow_none=True)

class TaskResponseSchema(Schema):
    id=fields.Int(dump_only=True)
    title=fields.Str()
    description=fields.Str(allow_none=True)
    completed=fields.Boolean()
    due_date=fields.DateTime(format="iso", allow_none=True)
    category_id=fields.Int()
    created_at=fields.DateTime(format="iso")
    updated_at=fields.DateTime(format="iso")

    @post_dump
    def normalize_utc_suffix(self, data, **kwargs):
        for key in ("due_date", "created_at", "updated_at"):
            value = data.get(key)
            if not isinstance(value, str):
                continue

            if value.endswith("+00:00"):
                data[key] = f"{value[:-6]}Z"
                continue

            suffix = value[10:] if len(value) > 10 else ""
            has_tz = suffix.endswith("Z") or "+" in suffix or "-" in suffix
            if "T" in value and not has_tz:
                data[key] = f"{value}Z"

        return data
