from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates

# Names our constraints so migrations work smoothly with SQLite
metadata = MetaData(naming_convention={
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Allowed exercise categories, used by the model and later by the schema
VALID_CATEGORIES = ['strength', 'cardio', 'flexibility', 'balance']


class Exercise(db.Model):
    __tablename__ = 'exercises'

    # TABLE CONSTRAINT: name can't be an empty string
    __table_args__ = (
        db.CheckConstraint("length(name) > 0", name="name_not_empty"),
    )

    id = db.Column(db.Integer, primary_key=True)
    # TABLE CONSTRAINT: no two exercises can have the same name
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    # An Exercise has many WorkoutExercises
    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan'
    )
    # An Exercise has many Workouts through WorkoutExercises
    workouts = association_proxy('workout_exercises', 'workout')

    # MODEL VALIDATION: name must not be blank
    @validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError("Exercise name cannot be empty.")
        return name.strip()

    # MODEL VALIDATION: category must be one of the allowed categories
    @validates('category')
    def validate_category(self, key, category):
        if not category or category.lower() not in VALID_CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(VALID_CATEGORIES)}.")
        return category.lower()

    def __repr__(self):
        return f'<Exercise {self.id}: {self.name}>'


class Workout(db.Model):
    __tablename__ = 'workouts'

    # TABLE CONSTRAINT: a workout must last more than 0 minutes
    __table_args__ = (
        db.CheckConstraint("duration_minutes > 0", name="duration_positive"),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    # A Workout has many WorkoutExercises
    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='workout', cascade='all, delete-orphan'
    )
    # A Workout has many Exercises through WorkoutExercises
    exercises = association_proxy('workout_exercises', 'exercise')

    # MODEL VALIDATION: duration must be a positive whole number
    @validates('duration_minutes')
    def validate_duration_minutes(self, key, minutes):
        if not isinstance(minutes, int) or minutes <= 0:
            raise ValueError("Duration must be a whole number greater than 0.")
        return minutes

    # MODEL VALIDATION: notes can't be longer than 500 characters
    @validates('notes')
    def validate_notes(self, key, notes):
        if notes and len(notes) > 500:
            raise ValueError("Notes cannot be longer than 500 characters.")
        return notes

    def __repr__(self):
        return f'<Workout {self.id}: {self.date}, {self.duration_minutes} mins>'


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    # TABLE CONSTRAINT: reps, sets and duration must be positive when given.
    # (In SQL, a check on an empty/NULL value passes, so these stay optional.)
    __table_args__ = (
        db.CheckConstraint("reps > 0", name="reps_positive"),
        db.CheckConstraint("sets > 0", name="sets_positive"),
        db.CheckConstraint("duration_seconds > 0", name="duration_seconds_positive"),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # A WorkoutExercise belongs to a Workout and an Exercise
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    # MODEL VALIDATION: reps, sets and duration must be positive if provided
    @validates('reps', 'sets', 'duration_seconds')
    def validate_positive_numbers(self, key, value):
        if value is not None and (not isinstance(value, int) or value <= 0):
            raise ValueError(f"{key} must be a whole number greater than 0.")
        return value

    def __repr__(self):
        return f'<WorkoutExercise workout={self.workout_id} exercise={self.exercise_id}>'