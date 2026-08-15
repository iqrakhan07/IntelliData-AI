import sqlite3
from datetime import datetime


DATABASE_PATH = "database/intellidata.db"


def get_connection():
    """
    Create and return SQLite database connection.
    """
    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )

    return connection


def initialize_database():
    """
    Create database tables if they don't exist.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # ---------------------------------------------
    # DATASETS TABLE
    # ---------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            rows INTEGER,
            columns INTEGER,
            uploaded_at TEXT
        )
    """)

    # ---------------------------------------------
    # EXPERIMENTS TABLE
    # ---------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS experiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_name TEXT,
            problem_type TEXT,
            algorithm TEXT,
            target_column TEXT,
            score REAL,
            created_at TEXT
        )
    """)

    # ---------------------------------------------
    # PREDICTIONS TABLE
    # ---------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_type TEXT,
            target_column TEXT,
            prediction TEXT,
            confidence REAL,
            created_at TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_dataset(
    filename,
    rows,
    columns
):
    """
    Save uploaded dataset information.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO datasets
        (
            filename,
            rows,
            columns,
            uploaded_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        filename,
        rows,
        columns,
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ))

    connection.commit()
    connection.close()


def save_experiment(
    dataset_name,
    problem_type,
    algorithm,
    target_column,
    score
):
    """
    Save ML experiment information.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO experiments
        (
            dataset_name,
            problem_type,
            algorithm,
            target_column,
            score,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        dataset_name,
        problem_type,
        algorithm,
        target_column,
        score,
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ))

    connection.commit()
    connection.close()


def save_prediction(
    model_type,
    target_column,
    prediction,
    confidence=None
):
    """
    Save prediction information.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO predictions
        (
            model_type,
            target_column,
            prediction,
            confidence,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        model_type,
        target_column,
        str(prediction),
        confidence,
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ))

    connection.commit()
    connection.close()


def get_datasets():
    """
    Get uploaded datasets.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM datasets
        ORDER BY id DESC
    """)

    results = cursor.fetchall()

    connection.close()

    return results


def get_experiments():
    """
    Get ML experiments.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM experiments
        ORDER BY id DESC
    """)

    results = cursor.fetchall()

    connection.close()

    return results


def get_predictions():
    """
    Get prediction history.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM predictions
        ORDER BY id DESC
    """)

    results = cursor.fetchall()

    connection.close()

    return results