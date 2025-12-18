import sqlite3

DB_PATH = "utils/db/pharmacy.db"

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

    cur.execute("""
    CREATE TABLE IF NOT EXISTS medications_sold (
      id TEXT PRIMARY KEY,                 -- UUID for this sale record
      medication_id TEXT NOT NULL,         -- FK to medications.id
      user_id TEXT,                        -- who bought it (nullable for OTC)
      prescription_id TEXT,               -- FK to prescriptions.id (nullable)
      quantity INTEGER NOT NULL,           -- units sold
      unit_price REAL,                     -- optional: price per unit
      total_price REAL,                    -- optional: quantity * unit_price
      sold_at TEXT NOT NULL,               -- ISO timestamp (YYYY-MM-DD HH:MM:SS)
      sold_year INTEGER NOT NULL,          -- for fast yearly stats
      sold_month INTEGER NOT NULL,         -- 1–12
      sold_day INTEGER NOT NULL            -- 1–31
    )
    """)

    c.commit()
    c.close()
