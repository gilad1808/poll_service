
from .poll_db import get_db_connection


def create_poll(question: str, options: list[str]):
    connection = get_db_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO polls (question) VALUES (%s)",
            (question,)
        )

        poll_id = cursor.lastrowid

        for option in options:
            cursor.execute(
                """
                INSERT INTO poll_options (poll_id, option_text)
                VALUES (%s, %s)
                """,
                (poll_id, option)
            )

        connection.commit()
        return poll_id

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def get_poll_by_id(poll_id: int):
    connection = get_db_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT id, question FROM polls WHERE id = %s",
            (poll_id,)
        )

        poll = cursor.fetchone()

        if poll is None:
            return None

        cursor.execute(
            """
            SELECT id, option_text
            FROM poll_options
            WHERE poll_id = %s
            """,
            (poll_id,)
        )

        options = cursor.fetchall()

        poll["options"] = options

        return poll

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

def get_vote_counts_by_poll_id(poll_id: int):
    connection = get_db_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                po.id AS option_id,
                po.option_text,
                COUNT(v.id) AS vote_count
            FROM poll_options AS po
            LEFT JOIN votes AS v ON v.option_id = po.id
            WHERE po.poll_id = %s
            GROUP BY po.id, po.option_text
            ORDER BY po.id
            """,
            (poll_id,),
        )
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

def get_all_poll_result_rows():
    connection = get_db_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                p.id AS poll_id,
                p.question,
                po.id AS option_id,
                po.option_text,
                COUNT(v.id) AS vote_count
            FROM polls AS p
            LEFT JOIN poll_options AS po ON po.poll_id = p.id
            LEFT JOIN votes AS v ON v.option_id = po.id
            GROUP BY p.id, p.question, po.id, po.option_text
            ORDER BY p.id, po.id
            """
        )
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

def get_answers_by_user_id(user_id: int):
    connection = get_db_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                p.id AS poll_id,
                p.question,
                po.id AS option_id,
                po.option_text
            FROM votes AS v
            JOIN polls AS p ON p.id = v.poll_id
            JOIN poll_options AS po ON po.id = v.option_id
            WHERE v.user_id = %s
            ORDER BY p.id
            """,
            (user_id,),
        )
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

def update_poll_question(poll_id: int, question: str):
    connection = get_db_connection()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE polls SET question = %s WHERE id = %s",
            (question, poll_id),
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

def delete_poll(poll_id: int) -> bool:
    connection = get_db_connection()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id FROM polls WHERE id = %s FOR UPDATE",
            (poll_id,),
        )
        if cursor.fetchone() is None:
            connection.rollback()
            return False

        cursor.execute("DELETE FROM votes WHERE poll_id = %s", (poll_id,))
        cursor.execute("DELETE FROM poll_options WHERE poll_id = %s", (poll_id,))
        cursor.execute("DELETE FROM polls WHERE id = %s", (poll_id,))
        connection.commit()
        return True
    except Exception:
        connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

def delete_votes_by_user_id(user_id: int) -> None:
    connection = get_db_connection()
    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM votes WHERE user_id = %s", (user_id,))
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

def create_vote(poll_id: int, option_id: int, user_id: int):
    connection = get_db_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO votes (poll_id, option_id, user_id)
            VALUES (%s, %s, %s)
            """,
            (poll_id, option_id, user_id)
        )

        vote_id = cursor.lastrowid

        connection.commit()

        return vote_id

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def get_option_by_id(option_id: int):
    connection = get_db_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, poll_id, option_text
            FROM poll_options
            WHERE id = %s
            """,
            (option_id,)
        )

        option = cursor.fetchone()

        return option

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def get_vote_by_user_and_poll(poll_id: int, user_id: int):
    connection = get_db_connection()
    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, poll_id, option_id, user_id
            FROM votes
            WHERE poll_id = %s AND user_id = %s
            """,
            (poll_id, user_id)
        )

        vote = cursor.fetchone()

        return vote

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def update_vote(poll_id: int, user_id: int, option_id: int):
    connection = get_db_connection()
    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE votes
            SET option_id = %s
            WHERE poll_id = %s AND user_id = %s
            """,
            (option_id, poll_id, user_id)
        )

        connection.commit()

        return cursor.rowcount

    except Exception:
        connection.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()
