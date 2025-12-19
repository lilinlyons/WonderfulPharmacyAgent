from utils.db.db import conn


def get_medications_sold():
    """
    Get all medications sold with medication details joined
    """
    c = conn()
    cur = c.cursor()

    cur.execute("""
        SELECT 
            ms.id,
            ms.medication_id,
            m.brand_name,
            m.generic_name,
            ms.user_id,
            ms.prescription_id,
            ms.quantity,
            ms.unit_price,
            ms.total_price,
            ms.sold_at,
            ms.sold_year,
            ms.sold_month,
            ms.sold_day
        FROM medications_sold ms
        LEFT JOIN medications m ON ms.medication_id = m.id
        ORDER BY ms.sold_at ASC
    """)

    rows = cur.fetchall()
    c.close()

    # Convert to list of dicts and add medication_name field
    result = []
    for row in rows:
        row_dict = dict(row)

        # Create medication_name from brand_name or generic_name
        medication_name = row_dict.get("brand_name") or row_dict.get("generic_name") or row_dict.get(
            "medication_id") or "Unknown"
        row_dict["medication_name"] = medication_name

        result.append(row_dict)

    return result