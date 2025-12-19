from utils.db.db import conn
import re

def get_medication_by_name(query: str):
    """
    Look up a medication by brand or generic name.
    """
    c = conn()
    cur = c.cursor()

    # Normalize text: lowercase + remove punctuation
    cleaned = re.sub(r"[^a-zA-Z0-9\s]", "", query.lower())
    words = cleaned.split()

    for word in words:
        # Skip very short words like "do", "you", "in"
        if len(word) < 3:
            continue

        like = f"%{word}%"

        cur.execute(
            """
            SELECT *
            FROM medications
            WHERE lower(brand_name) LIKE ?
               OR lower(generic_name) LIKE ?
            LIMIT 1
            """,
            (like, like),
        )

        row = cur.fetchone()
        if row:
            return {
                "id": row["id"],
                "name": row["brand_name"],
                "generic_name": row["generic_name"],
                "active_ingredient": row["active_ingredient"],
                "rx_required": bool(row["rx_required"]),
                "form": row["form"],
                "strength": row["strength"],
                "label_instructions_en": row["label_instructions"],
                "warnings_en": row["warnings"]
            }

    return None
