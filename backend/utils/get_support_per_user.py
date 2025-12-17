from workflows.db.db import conn

def get_support_per_user(user_id: str):
    try:
        c = conn()
        cur = c.cursor()

        cur.execute(
            """
            SELECT
              id,
              subject,
              message,
              status,  
              created_at
            FROM support_requests
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,),
        )

        rows = cur.fetchall()
        c.close()

        return [
            {
                "id": row["id"],
                "subject": row["subject"],
                "message": row["message"],
                "status": row["status"],
                "created_at": row["created_at"],
            }
            for row in rows
        ]



    except Exception as e:
        return []
