import sqlite3

DB_PATH = "workflows/db/pharmacy.db"

def conn():
    c = sqlite3.connect(DB_PATH, check_same_thread=False)
    c.row_factory = sqlite3.Row
    print("Connection Successful")
    return c

def init_schema():
    c = conn()
    cur = c.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
      id TEXT PRIMARY KEY,
      full_name TEXT,
      phone TEXT,
      preferred_lang TEXT,
      role TEXT
    )""")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS medications (
          id TEXT PRIMARY KEY,
          brand_name TEXT,
          generic_name TEXT,
          active_ingredient TEXT,
          rx_required INTEGER,
          form TEXT,
          strength TEXT,
          label_instructions TEXT,
          warnings TEXT
        )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS support_requests (
      id TEXT PRIMARY KEY,
      user_id TEXT,
      subject TEXT,
      message TEXT,
      status TEXT,  
      created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS prescription_requests (
      id TEXT PRIMARY KEY,
      user_id TEXT,
      medication_id TEXT,
      request_type TEXT,    
      status TEXT,         
      notes TEXT,
      created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS stock (
      store_id TEXT,
      medication_id TEXT,
      quantity INTEGER,
      PRIMARY KEY (store_id, medication_id)
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS prescriptions (
      id TEXT PRIMARY KEY,
      user_id TEXT,
      medication_id TEXT,
      status TEXT,      
      refills_left INTEGER,
      expires_on TEXT
    )""")


    c.commit()
    c.close()
