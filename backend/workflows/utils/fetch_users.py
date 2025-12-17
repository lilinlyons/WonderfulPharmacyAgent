from workflows.db.db import conn


def fetch_users():
    """
    Fetch all users for UI selection.
    """
    c = conn()
    cur = c.cursor()

    cur.execute(
        """
        SELECT id, full_name, phone, preferred_lang, role
        FROM users
        ORDER BY full_name
        """
    )

    rows = cur.fetchall()
    c.close()

    if not rows:
        return []

    return [
        {
            "id": row["id"],
            "full_name": row["full_name"],
            "phone": row["phone"],
            "preferred_lang": row["preferred_lang"],
            "role": row["role"],
        }
        for row in rows
    ]
