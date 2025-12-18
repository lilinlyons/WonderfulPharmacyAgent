from utils.db.db import conn
from fastapi import HTTPException

def update_prescription_request_status(prescription_id: str, status: str):
    c = conn()
    cur = c.cursor()

    cur.execute(
        """
        UPDATE prescription_requests
        SET status = ?
        WHERE id = ?
        """,
        (status, prescription_id),
    )

    if cur.rowcount == 0:
        c.close()
        raise HTTPException(status_code=404, detail="Prescription not found")

    c.commit()
    c.close()
