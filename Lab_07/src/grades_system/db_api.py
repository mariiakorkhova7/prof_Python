import sqlite3

def get_student_subject_stats(database_path: str, student_id: int, subject_id: int) -> tuple:
    """Використання SQL AVG(), MIN(), MAX() через DB-API[cite: 32]."""
    with sqlite3.connect(database_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT AVG(value), MIN(value), MAX(value)
            FROM grades
            WHERE student_id = ? AND subject_id = ?
            """,
            (student_id, subject_id)
        )
        return cursor.fetchone()