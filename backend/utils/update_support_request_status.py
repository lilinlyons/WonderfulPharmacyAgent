from workflows.db.db import conn
from fastapi import HTTPException

def update_support_request_status(support_id: str, status: str):
    c = conn()
    cur = c.cursor()

    cur.execute(
        """
        UPDATE support_requests
        SET status = ?
        WHERE id = ?
        """,
        (status, support_id),
    )

    if cur.rowcount == 0:
        c.close()
        raise HTTPException(status_code=404, detail="Support request not found")

    c.commit()
    c.close()
