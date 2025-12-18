from utils.db.db import conn

def get_medications_sold():
    c = conn()
    cur = c.cursor()

    cur.execute("""
        SELECT
          id,
          medication_id,
          user_id,
          prescription_id,
          quantity,
          unit_price,
          total_price,
          sold_at,
          sold_year,
          sold_month,
          sold_day
        FROM medications_sold
        ORDER BY sold_at ASC
    """)

    rows = cur.fetchall()
    c.close()

    return [dict(row) for row in rows]
