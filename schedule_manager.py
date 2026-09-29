from database import get_connection


def add_subject(name, exam_date, priority=1):

    connection = get_connection()

    cursor = connection.cursor()

    query = """
        INSERT INTO subjects
        (name, exam_date, priority)
        VALUES (%s, %s, %s)
        RETURNING id
    """

    cursor.execute(
        query,
        (name, exam_date, priority)
    )

    subject_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return subject_id


def get_subjects():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            exam_date,
            priority
        FROM subjects
        ORDER BY exam_date NULLS LAST
    """)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    subjects = []

    for row in rows:

        subjects.append({
            "id": row[0],
            "name": row[1],
            "exam_date": str(row[2]) if row[2] else None,
            "priority": row[3]
        })

    return subjects


def add_task(
    subject_id,
    topic,
    due_date,
    duration=60
):

    connection = get_connection()

    cursor = connection.cursor()

    query = """
        INSERT INTO study_tasks
        (subject_id, topic, due_date, duration)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """

    cursor.execute(
        query,
        (
            subject_id,
            topic,
            due_date,
            duration
        )
    )

    task_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return task_id


def get_pending_tasks():

    connection = get_connection()

    cursor = connection.cursor()

    query = """
        SELECT
            study_tasks.id,
            subjects.name,
            study_tasks.topic,
            study_tasks.due_date,
            study_tasks.duration,
            study_tasks.status

        FROM study_tasks

        JOIN subjects
        ON study_tasks.subject_id = subjects.id

        WHERE study_tasks.status = 'pending'

        ORDER BY study_tasks.due_date NULLS LAST
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    tasks = []

    for row in rows:

        tasks.append({
            "id": row[0],
            "subject": row[1],
            "topic": row[2],
            "due_date": str(row[3]) if row[3] else None,
            "duration": row[4],
            "status": row[5]
        })

    return tasks


def complete_task(task_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE study_tasks
        SET status = 'completed'
        WHERE id = %s
    """, (task_id,))

    connection.commit()

    updated = cursor.rowcount

    cursor.close()
    connection.close()

    return updated