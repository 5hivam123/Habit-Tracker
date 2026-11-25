# Habit Tracker

A web-based habit tracking application built with Python and Flask. The application allows users to create, manage, and analyze personal habits with daily or weekly periodicity through a modern browser interface.

## Features

* Create, complete, and delete habits via a web dashboard
* Daily and weekly habit tracking
* View habit details and completion history
* Track completion streaks with a visual leaderboard
* Analyze the longest streaks across all or specific habits
* Habits grouped by periodicity (daily/weekly)
* Persistent storage using SQLite
* Predefined demo data with four weeks of example tracking data
* Unit tests for core habit behaviour and analytics

## Requirements

* Python 3.10 or later (3.13+ preferred)
* Flask (`pip install flask`)

## Setup

Clone the repository and install Flask:

```
git clone https://github.com/delta6626/habit-tracker-project
cd habit-tracker-project
pip install flask
```

## Running the Application

Start the web server from the project root:

```
python web_app.py
```

Then open **http://localhost:5000** in your browser.

## Usage

The web dashboard provides:

| Feature | Description |
| ------- | ----------- |
| **Dashboard** (`/`) | View all habits with streak counts, check off habits, add new ones, delete existing ones |
| **Analytics** (`/analytics`) | Streak leaderboard, best streak overall, habits grouped by periodicity |
| **Habit Detail** (click a habit name) | Full completion history, streak info, creation date, and metadata |

**Creating a habit:** Fill in the name, optional description, and periodicity (daily or weekly) in the form at the top of the dashboard, then click "Add Habit".

**Completing a habit:** Click the "✓ Check Off" button on any habit card.

**Deleting a habit:** Click the "✕" button on any habit card and confirm the deletion.

## Demo Data

On the first run, the application automatically loads five predefined habits with four weeks of example tracking data:

| Habit | Periodicity |
| ----- | ----------- |
| Drink water | Daily |
| Daily run | Daily |
| Daily meditation | Daily |
| Read a book | Weekly |
| Learn CS | Weekly |

This data is used for testing purposes and also gives new users something to interact with. It can be deleted through the web interface like any other habit.

If the demo data has been deleted or modified and you want to restore it to its original state, open `config.json` and set the `demo_data_loaded` flag to `false`:

```
{"demo_data_loaded": false}
```

The original demo data will then be loaded the next time the application is started.

**Note: The config.json file is not created until the application has run for the first time.**

## Running the Tests

Run the unit tests from the project root:

```
python -m unittest ./tests/test_habit.py ./tests/test_analytics.py
```

## Project Structure

```
habit-tracker-project/
├── web_app.py          # Flask web server and routes
├── Habit.py            # Habit domain model
├── analytics.py        # Streak calculation and reporting
├── constants.py        # SQL queries and type definitions
├── utilities.py        # Demo data seeding and config
├── templates/
│   └── index.html      # Web UI template
├── tests/
│   ├── test_habit.py
│   └── test_analytics.py
├── .gitignore
├── LICENSE.md
└── README.md
```

## License

See [LICENSE.md](LICENSE.md) for details.
