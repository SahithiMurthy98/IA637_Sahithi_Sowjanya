Fitness Tracker Web Application

A Flask-based fitness tracking system that allows administrators to create workout plans and track customer activity. Users can sign up, view plans, start or complete workouts, and view analytics based on usage.

✨ Features

▶ Admin:

-Add/update/delete workouts and plans

-Link multiple workouts to each plan (many-to-many)

-View user statistics (total users, by gender)

▶ Customer:

View available plans

Start or complete a plan

Start and stop workouts under a plan

Activity logs recorded for all actions

▶ Analytics:

Bar chart showing total users and users by gender

Admin dashboard shows insights upon login

♻ Tech Stack

Backend: Flask (Python)

Database: MySQL (with PyMySQL)

Frontend: HTML, CSS, Jinja2 templates, JavaScript

Visualization: Chart.js

📂 Folder Structure

flask_template/
|├─ app.py                # Main Flask app and routes
|├─ config.yml            # Table and DB mappings
|├─ user.py               # User model and validation
|├─ plan.py               # Plan model
|├─ workout.py            # Workout model
|├─ planworkout.py        # Logic to connect workouts to plans
|├─ activitylog.py        # Activity logging logic
|├─ templates/           # HTML pages and layouts
|└─ static/              # CSS and JS files

⚖ Database Schema Overview

plans

Column

Type

planid

INT, PK

planname

VARCHAR(100)

status

VARCHAR(20)

workouts

Column

Type

workoutid

INT, PK

workoutname

VARCHAR(100)

category

VARCHAR(50)

planworkouts (join table)

| planworkoutid | INT, PK      |
| planid        | FK -> plans  |
| workoutid     | FK -> workouts |

activitylog

| activityid | INT, PK     |
| userid     | FK -> user  |
| planid     | FK -> plans |
| workoutid  | FK -> workouts |
| starttime  | DATETIME    |
| endtime    | DATETIME    |

📗 How to Run

Ensure Python 3.11+ is installed

Set up a MySQL database and import schema tables

Update config.yml with your DB credentials

Run:

python app.py

Visit http://localhost:5000/ in browser

⚡ Future Improvements

Workout difficulty & duration fields

Plan-based progress tracking (percentage)

Monthly usage reports

Export user logs as CSV
