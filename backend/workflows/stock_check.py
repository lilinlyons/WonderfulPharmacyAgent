# workflows/inventory.py
from workflows.db.db import conn
from workflows.utils.fetch_medication import get_medication_by_name
from utils.workflow_logger import get_workflow_logger

logger = get_workflow_logger()

def handle(message: str):
    logger.info("Workflow started")
    logger.info("Input message: %s", message)

    try:
        med = get_medication_by_name(message)
    except Exception:
        logger.exception("Failed to fetch medication")
        return {
            "type": "inventory",
            "context": (
                "Sorry, there was an internal error while retrieving the medication information."
            )
        }

    if not med:
        logger.info("Medication not found")
        return {
            "type": "inventory",
            "context": "Medication not found in the system."
        }

    try:
        stock_by_store = check_stock_per_store(medication_id=med["id"])
    except Exception:
        logger.exception(
            "Failed to fetch inventory for medication_id=%s",
            med.get("id"),
        )
        return {
            "type": "inventory",
            "context": (
                "Sorry, there was an internal error while checking inventory availability."
            )
        }

    if not stock_by_store:
        logger.info("Medication not available in any store")
        return {
            "type": "inventory",
            "context": (
                f"Medication name: {med['name']}\n"
                "Stock status: Not available in any store."
            )
        }

    logger.info(
        "Inventory found for medication: name=%s stores=%d",
        med.get("name"),
        len(stock_by_store),
    )

    # Build readable inventory list
    inventory_lines = []
    for row in stock_by_store:
        status = "In stock" if row["quantity"] > 0 else "Out of stock"
        inventory_lines.append(
            f"- Store {row['store_id']}: {status} (Qty: {row['quantity']})"
        )

    return {
        "type": "inventory",
        "context": (
            f"Medication name: {med['name']}\n"
            "Availability by store:\n"
            f"{chr(10).join(inventory_lines)}"
        )
    }


def check_stock_per_store(medication_id: str):
    """
    Return stock levels for a medication across all stores.
    """
    logger.info("Checking stock per store for medication_id=%s", medication_id)

    c = None
    try:
        c = conn()
        cur = c.cursor()

        cur.execute(
            """
            SELECT store_id, quantity
            FROM stock
            WHERE medication_id = ?
            ORDER BY store_id
            """,
            (medication_id,),
        )

        rows = cur.fetchall()
    except Exception:
        logger.exception(
            "Database error while fetching stock for medication_id=%s",
            medication_id,
        )
        raise
    finally:
        if c:
            c.close()

    if not rows:
        return []

    return [
        {
            "store_id": row["store_id"],
            "quantity": row["quantity"],
        }
        for row in rows
    ]
