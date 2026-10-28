# Workout Tracker API

A Flask backend API for a workout tracking application used by personal trainers. Trainers can create workouts and reusable exercises, then add exercises to workouts with reps, sets and/or duration.

Built with Flask, SQLAlchemy, Flask-Migrate and Marshmallow.

## Data Model

- **Exercise**: `id`, `name`, `category`, `equipment_needed`
- **Workout**: `id`, `date`, `duration_minutes`, `notes`
- **WorkoutExercise** (join table): `id`, `workout_id`, `exercise_id`, `reps`, `sets`, `duration_seconds`

A Workout has many Exercises through WorkoutExercises, and an Exercise has many Workouts through WorkoutExercises. Deleting a Workout or Exercise also deletes its WorkoutExercises.

## Validations

**Table constraints**
- Exercise `name` must be unique and not empty
- Workout `duration_minutes` must be greater than 0
- WorkoutExercise `reps`, `sets` and `duration_seconds` must be greater than 0 when provided

**Model validations**
- Exercise `name` cannot be blank
- Exercise `category` must be one of: strength, cardio, flexibility, balance
- Workout `duration_minutes` must be a positive whole number
- Workout `notes` cannot exceed 500 characters
- WorkoutExercise `reps`, `sets` and `duration_seconds` must be positive whole numbers

**Schema validations**
- Exercise `name` must be 1 to 100 characters
- Exercise `category` must be one of the allowed categories
- Workout `duration_minutes` must be between 1 and 600
- Workout `date` cannot be in the future
- Workout `notes` cannot exceed 500 characters
- WorkoutExercise must include at least one of `reps`, `sets` or `duration_seconds`

## Installation

1. Clone the repository:

```bash
   git clone <your-repo-url>
   cd workout-tracker-api
```

2. Install dependencies and activate the virtual environment:

```bash
   pipenv install
   pipenv shell
```

3. Move into the server directory and set the Flask app:

```bash
   cd server
   export FLASK_APP=app.py        # macOS/Linux
   set FLASK_APP=app.py           # Windows Command Prompt
```

4. Create the database and seed it:

```bash
   flask db upgrade head
   python seed.py
```

   The seed file clears existing data first, so it can be rerun at any time to reset the database.

## Running the App

From the `server` directory:

```bash
flask run --port 5555
```

The API will be available at `http://127.0.0.1:5555`.

## Endpoints

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Show a workout with its exercises, including reps, sets and duration |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<id>` | Delete a workout and its associated WorkoutExercises |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Show an exercise with the workouts it appears in |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise and its associated WorkoutExercises |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout with reps, sets and/or duration |

### Example request bodies

**POST `/workouts`**

```json
{
  "date": "2026-10-27",
  "duration_minutes": 50,
  "notes": "Full body session"
}
```

**POST `/exercises`**

```json
{
  "name": "Lunge",
  "category": "strength",
  "equipment_needed": false
}
```

**POST `/workouts/1/exercises/2/workout_exercises`**

```json
{
  "reps": 12,
  "sets": 3
}
```

### Responses

- `200` successful GET
- `201` resource created
- `204` resource deleted (empty body)
- `400` validation error, with error messages in the response body
- `404` workout or exercise not found