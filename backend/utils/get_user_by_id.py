from utils.db.db import conn


def get_user_by_id(user_id: str) -> dict | None:
    """
    Returns a single user by ID or None if not found.
    """
    try:
        c = conn()
        c.row_factory = lambda cursor, row: {
            col[0]: row[idx] for idx, col in enumerate(cursor.description)
        }
        cur = c.cursor()

        cur.execute(
            """
            SELECT
              id,
              full_name,
              phone,
              preferred_lang,
              role
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        )

        row = cur.fetchone()
        c.close()

        return row  # dict or None

    except Exception as e:
        # optionally log this
        return None
