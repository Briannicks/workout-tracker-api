from datetime import date

from marshmallow import Schema, fields, validate, validates, validates_schema, ValidationError

from models import VALID_CATEGORIES


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category = fields.Str(required=True, validate=validate.OneOf(VALID_CATEGORIES))
    equipment_needed = fields.Bool(load_default=False)
    workout_exercises = fields.Nested(
        lambda: WorkoutExerciseSchema(exclude=('exercise',)),
        many=True,
        dump_only=True,
    )


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(strict=True, allow_none=True, validate=validate.Range(min=1))
    sets = fields.Int(strict=True, allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(strict=True, allow_none=True, validate=validate.Range(min=1))

    # "only" limits nested fields so the nesting doesn't loop forever
    exercise = fields.Nested(
        lambda: ExerciseSchema(only=('id', 'name', 'category', 'equipment_needed')),
        dump_only=True,
    )
    workout = fields.Nested(
        lambda: WorkoutSchema(only=('id', 'date', 'duration_minutes', 'notes')),
        dump_only=True,
    )

    @validates_schema
    def validate_has_amount(self, data, **kwargs):
        if (
            data.get('reps') is None
            and data.get('sets') is None
            and data.get('duration_seconds') is None
        ):
            raise ValidationError('Provide at least one of reps, sets or duration_seconds.')


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(
        required=True, strict=True, validate=validate.Range(min=1, max=600)
    )
    notes = fields.Str(allow_none=True, validate=validate.Length(max=500))
    workout_exercises = fields.Nested(
        WorkoutExerciseSchema(exclude=('workout',)),
        many=True,
        dump_only=True,
    )

    @validates('date')
    def validate_date(self, value):
        if value > date.today():
            raise ValidationError('Workout date cannot be in the future.')