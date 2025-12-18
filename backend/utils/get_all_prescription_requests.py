from utils.db.db import conn

def get_all_prescription_requests():
    c = conn()
    cur = c.cursor()

    cur.execute("""
        SELECT *
        FROM prescription_requests
        ORDER BY created_at DESC
    """)

    rows = cur.fetchall()
    c.close()
    return [dict(row) for row in rows]
