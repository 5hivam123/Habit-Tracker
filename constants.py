"""
Constants used throughout the application.
"""

from typing import Literal

################# TYPE DEFINITIONS #################

Periodicity = Literal["daily", "weekly"]
PERIODICITY_DAY_COUNT: dict[Periodicity, int] = {"daily": 1, "weekly": 7}

################# TEST DATA IDs #################

RECORD_IDS = ["TDR1", "TDR2", "TDR3", "TDR4", "TDR5"]

################# DATABASE #################

MAIN_TABLE_NAME = "habits"
COMPLETIONS_TABLE_NAME = "completions"

GET_ALL_HABITS_SQL = f"""
SELECT * FROM {MAIN_TABLE_NAME}
"""

GET_HABIT_COMPLETIONS_SQL = f"""
SELECT completed_at
FROM {COMPLETIONS_TABLE_NAME}
WHERE habit_id = ?
"""

CREATE_HABITS_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {MAIN_TABLE_NAME} (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    periodicity TEXT NOT NULL,
    created_at TEXT NOT NULL
)
"""

CREATE_COMPLETIONS_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {COMPLETIONS_TABLE_NAME} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id TEXT NOT NULL,
    completed_at TEXT NOT NULL,
    FOREIGN KEY (habit_id) REFERENCES {MAIN_TABLE_NAME}(id) ON DELETE CASCADE
)
"""

INSERT_HABIT_SQL = f"""
INSERT INTO {MAIN_TABLE_NAME} (
    id,
    name,
    description,
    periodicity,
    created_at
)
VALUES (?, ?, ?, ?, ?)
"""

CHECK_OFF_HABIT_SQL = f"""
INSERT INTO {COMPLETIONS_TABLE_NAME} (
    habit_id,
    completed_at
)
VALUES (?, ?)
"""

DELETE_HABIT_SQL = f"""
DELETE FROM {MAIN_TABLE_NAME}
WHERE id = ?
"""

DELETE_DEMO_DATA_SQL = f"""
DELETE FROM {MAIN_TABLE_NAME}
WHERE ID IN ({', '.join(f"'{id}'" for id in RECORD_IDS)})
"""
