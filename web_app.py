"""
Web interface for the Habit Tracker application.
Wraps the existing CLI logic into a Flask web server.
"""

import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, g
from datetime import datetime
from Habit import Habit
import analytics
import constants
from utilities import is_demo_data_loaded, update_demo_data_status, seed_demo_data

app = Flask(__name__)
app.secret_key = "habit-tracker-secret-key"

DB_PATH = "habit_database.db"


def get_db():
    """Get a database connection for the current request thread."""
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(exception):
    """Close the database connection at the end of each request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Initialize tables and seed demo data if needed."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    cursor.execute(constants.CREATE_HABITS_TABLE_SQL)
    cursor.execute(constants.CREATE_COMPLETIONS_TABLE_SQL)
    if not is_demo_data_loaded():
        seed_demo_data(cursor, datetime(2026, 9, 20, 12, 0, 0))
        update_demo_data_status(True)
    conn.commit()
    conn.close()


def load_habits_from_db(db):
    """Load all habits from the database."""
    cursor = db.cursor()
    cursor.execute(constants.GET_ALL_HABITS_SQL)
    habits = cursor.fetchall()
    habit_objects = []
    for habit in habits:
        habit_id, name, description, periodicity, created_at = habit
        cursor.execute(constants.GET_HABIT_COMPLETIONS_SQL, (habit_id,))
        completions = [datetime.fromisoformat(row[0]) for row in cursor.fetchall()]
        habit_objects.append(
            Habit(habit_id, name, description, periodicity,
                  datetime.fromisoformat(created_at), completions)
        )
    return habit_objects


def get_sorted_habits(db):
    """Return habits sorted by creation date, newest first."""
    habits = load_habits_from_db(db)
    return sorted(habits, key=lambda h: h.created_at, reverse=True)


@app.route("/")
def index():
    """Main dashboard showing all habits."""
    db = get_db()
    sorted_habits = get_sorted_habits(db)

    habits_data = []
    for habit in sorted_habits:
        streak = analytics.get_longest_streak_for_habit(habit)
        last_completion = max(habit.completions) if habit.completions else None
        habits_data.append({
            "habit": habit,
            "streak": streak,
            "completions_count": len(habit.completions),
            "last_completion": last_completion,
        })

    return render_template("index.html", habits_data=habits_data)


@app.route("/add", methods=["POST"])
def add_habit():
    """Add a new habit."""
    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip()
    periodicity = request.form.get("periodicity", "daily")

    if not name:
        flash("Habit name cannot be empty.", "error")
        return redirect(url_for("index"))

    db = get_db()
    new_habit = Habit(None, name, description, periodicity, datetime.now(), [])
    cursor = db.cursor()
    cursor.execute(
        constants.INSERT_HABIT_SQL,
        (new_habit.id, new_habit.name, new_habit.description,
         new_habit.periodicity, new_habit.created_at.isoformat()),
    )
    db.commit()
    flash(f"Habit '{name}' added successfully!", "success")
    return redirect(url_for("index"))


@app.route("/complete/<habit_id>", methods=["POST"])
def complete_habit(habit_id):
    """Check off a habit."""
    db = get_db()
    current_time = datetime.now()
    cursor = db.cursor()
    cursor.execute(constants.CHECK_OFF_HABIT_SQL, (habit_id, current_time.isoformat()))
    db.commit()

    # Get habit name for the flash message
    habits = load_habits_from_db(db)
    habit_name = next((h.name for h in habits if h.id == habit_id), "Habit")
    flash(f"'{habit_name}' checked off!", "success")
    return redirect(url_for("index"))


@app.route("/delete/<habit_id>", methods=["POST"])
def delete_habit(habit_id):
    """Delete a habit."""
    db = get_db()
    # Get habit name before deleting
    habits = load_habits_from_db(db)
    habit_name = next((h.name for h in habits if h.id == habit_id), "Habit")

    cursor = db.cursor()
    cursor.execute(constants.DELETE_HABIT_SQL, (habit_id,))
    db.commit()
    flash(f"'{habit_name}' deleted.", "success")
    return redirect(url_for("index"))


@app.route("/analytics")
def view_analytics():
    """Analytics dashboard."""
    db = get_db()
    sorted_habits = get_sorted_habits(db)

    if sorted_habits:
        best_habit, best_streak = analytics.get_longest_streak_overall(sorted_habits)
    else:
        best_habit, best_streak = None, 0

    streaks = []
    for habit in sorted_habits:
        streak = analytics.get_longest_streak_for_habit(habit)
        streaks.append({"habit": habit, "streak": streak})

    daily_habits = [h for h in sorted_habits if h.periodicity == "daily"]
    weekly_habits = [h for h in sorted_habits if h.periodicity == "weekly"]

    return render_template(
        "index.html",
        habits_data=[{
            "habit": h,
            "streak": analytics.get_longest_streak_for_habit(h),
            "completions_count": len(h.completions),
            "last_completion": max(h.completions) if h.completions else None,
        } for h in sorted_habits],
        show_analytics=True,
        best_habit=best_habit,
        best_streak=best_streak,
        streaks=streaks,
        daily_habits=daily_habits,
        weekly_habits=weekly_habits,
    )


@app.route("/habit/<habit_id>")
def habit_detail(habit_id):
    """View detailed info for a single habit."""
    db = get_db()
    habits = load_habits_from_db(db)
    for habit in habits:
        if habit.id == habit_id:
            streak = analytics.get_longest_streak_for_habit(habit)
            return render_template(
                "index.html",
                habits_data=[{
                    "habit": habit,
                    "streak": streak,
                    "completions_count": len(habit.completions),
                    "last_completion": max(habit.completions) if habit.completions else None,
                }],
                detail_habit=habit,
                detail_streak=streak,
            )
    flash("Habit not found.", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    print("\n  Habit Tracker Web App")
    print("  Open http://localhost:5000 in your browser\n")
    app.run(debug=False, host="127.0.0.1", port=5000)
