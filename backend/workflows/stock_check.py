import re

from workflows.db.db import conn
from workflows.utils.fetch_medication import get_medication_by_name

def handle(message: str):
    med = get_medication_by_name(message)
    print("med:", med)
    print("checking stock")
    stock = check_stock(medication_id=med["id"])
    return {
        "type": "inventory",
        "context": f"""
Medication name: {med['name']}
Stock status: {stock['status']}
Available quantity: {stock.get('quantity', 'unknown')}
"""
    }

def check_stock(medication_id: str):
    """
    Check stock for a medication in a specific store.
    """
    c = conn()
    cur = c.cursor()

    cur.execute(
        """
        SELECT quantity
        FROM stock
        WHERE medication_id = ?

        """,
        (medication_id, ),
    )

    row = cur.fetchone()
    c.close()

    if not row:
        return {
            "status": "unknown",
            "quantity": None,
        }

    qty = row["quantity"]

    return {
        "status": "in_stock" if qty > 0 else "out_of_stock",
        "quantity": qty,
    }
