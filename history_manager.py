import sqlite3
from datetime import datetime
import os


DATABASE_NAME = "ecoscan.db"


# ============================================================
# Initialize Database
# ============================================================

def init_database():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            waste_type TEXT NOT NULL,
            confidence REAL NOT NULL,
            action TEXT NOT NULL,
            eco_score INTEGER NOT NULL,
            image_path TEXT,
            location TEXT,
            college TEXT,
            biotech_potential TEXT,
            environmental_level TEXT
        )
    """)

    connection.commit()

    # ========================================================
    # Safe Migration
    # ========================================================

    cursor.execute(
        "PRAGMA table_info(analysis_history)"
    )

    existing_columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    new_columns = {
        "image_path": "TEXT",
        "location": "TEXT",
        "college": "TEXT",
        "biotech_potential": "TEXT",
        "environmental_level": "TEXT"
    }

    for column_name, column_type in new_columns.items():

        if column_name not in existing_columns:

            cursor.execute(
                f"""
                ALTER TABLE analysis_history
                ADD COLUMN {column_name} {column_type}
                """
            )

    connection.commit()
    connection.close()


# ============================================================
# Save Analysis
# ============================================================

def save_analysis(
    waste_type,
    confidence,
    action,
    eco_score,
    image_path=None,
    location="Personal Scan",
    college=None,
    biotech_potential=None,
    environmental_level=None
):

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO analysis_history
        (
            timestamp,
            waste_type,
            confidence,
            action,
            eco_score,
            image_path,
            location,
            college,
            biotech_potential,
            environmental_level
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        waste_type,
        confidence,
        action,
        eco_score,
        image_path,
        location,
        college,
        biotech_potential,
        environmental_level
    ))

    connection.commit()
    connection.close()


# ============================================================
# Get Analysis History
# ============================================================

def get_history():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            timestamp,
            waste_type,
            confidence,
            action,
            eco_score,
            image_path,
            location,
            college,
            biotech_potential,
            environmental_level
        FROM analysis_history
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    connection.close()

    return records


# ============================================================
# Delete Analysis
# ============================================================

def delete_analysis(analysis_id):

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # Get image path before deleting
    cursor.execute("""
        SELECT image_path
        FROM analysis_history
        WHERE id = ?
    """, (analysis_id,))

    result = cursor.fetchone()

    # Delete database record
    cursor.execute("""
        DELETE FROM analysis_history
        WHERE id = ?
    """, (analysis_id,))

    connection.commit()
    connection.close()

    # Delete saved image if it exists
    if result and result[0]:

        image_path = result[0]

        if os.path.exists(image_path):

            try:
                os.remove(image_path)
            except OSError:
                pass


# ============================================================
# Clear All History
# ============================================================

def clear_history():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    # Get all image paths
    cursor.execute("""
        SELECT image_path
        FROM analysis_history
        WHERE image_path IS NOT NULL
    """)

    image_paths = cursor.fetchall()

    # Delete records
    cursor.execute(
        "DELETE FROM analysis_history"
    )

    connection.commit()
    connection.close()

    # Delete saved images
    for row in image_paths:

        image_path = row[0]

        if image_path and os.path.exists(image_path):

            try:
                os.remove(image_path)
            except OSError:
                pass
