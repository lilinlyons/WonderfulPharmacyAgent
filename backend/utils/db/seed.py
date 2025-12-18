from db import conn, init_schema

def seed():
    init_schema()
    c = conn()
    cur = c.cursor()

    users = [
        ("u1", "אור לוי", "050-1111111", "he", "customer"),
        ("u2", "דנה כהן", "050-2222222", "he", "customer"),
        ("u3", "נועם דוד", "050-3333333", "he", "customer"),
        ("u4", "Maya Katz", "050-4444444", "en", "customer"),
        ("u5", "איתן בר", "050-5555555", "he", "customer"),
        ("u6", "יעל אזולאי", "050-6666666", "he", "customer"),
        ("u7", "Tom Green", "050-7777777", "en", "pharmacist"),
        ("u8", "שירה מלכה", "050-8888888", "he", "customer"),
        ("u9", "אבי רון", "050-9999999", "he", "customer"),
        ("u10", "Liam Stone", "050-1010101", "en", "customer"),
    ]

    cur.executemany("INSERT OR REPLACE INTO users VALUES (?,?,?,?,?)", users)

    meds = [
        (
            "m1",
            "Acamol",
            "Paracetamol",
            "Paracetamol",
            0,
            "Tablet",
            "500mg",
            "Adults: follow package directions. Do not exceed the maximum daily dose on label.",
            "Do not use with other products containing paracetamol. Seek help if overdose suspected."
        ),
        (
            "m2",
            "Nurofen",
            "Ibuprofen",
            "Ibuprofen",
            0,
            "Capsule",
            "200mg",
            "Take with food or water as directed on label. Do not exceed label maximum.",
            "May not be suitable with certain conditions or medications. Ask a pharmacist or doctor."
        ),
        (
            "m3",
            "Augmentin",
            "Amoxicillin/Clavulanate",
            "Amoxicillin + Clavulanate",
            1,
            "Tablet",
            "875/125mg",
            "Prescription-only antibiotic. Use exactly as prescribed; complete the course.",
            "Allergy risk (penicillins). Seek urgent help for severe allergic reaction signs."
        ),
        (
            "m4",
            "Ventolin",
            "Salbutamol",
            "Salbutamol",
            1,
            "Inhaler",
            "100mcg/dose",
            "Prescription-only. Use exactly as prescribed. Refer to device instructions.",
            "If breathing worsens or relief is inadequate, seek urgent medical help."
        ),
        (
            "m5",
            "Claritin",
            "Loratadine",
            "Loratadine",
            0,
            "Tablet",
            "10mg",
            "Once daily as directed on label.",
            "May cause drowsiness in some people. Check label warnings."
        ),
        (
            "m6",
            "Glucophage",
            "Metformin",
            "Metformin",
            1,
            "Tablet",
            "500mg",
            "Take with meals to reduce stomach upset. Use exactly as directed by your physician.",
            "May cause gastrointestinal side effects. Rare risk of lactic acidosis. Monitor kidney function."
        )
    ]

    cur.executemany(
        """
        INSERT OR REPLACE INTO medications
        (id, brand_name, generic_name, active_ingredient, rx_required, form, strength, label_instructions, warnings)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        meds
    )

    stock_rows = [
      ("store_tlv","m1",42),("store_tlv","m2",15),("store_tlv","m3",5),("store_tlv","m4",0),("store_tlv","m5",18),
      ("store_jlm","m1",10),("store_jlm","m2",0),("store_jlm","m3",2),("store_jlm","m4",7),("store_jlm","m5",4),
    ]
    cur.executemany("INSERT OR REPLACE INTO stock VALUES (?,?,?)", stock_rows)

    prescriptions = [
      ("p1","u1","m3","active",1,"2026-03-01"),
      ("p2","u1","m4","expired",0,"2025-10-10"),
      ("p3","u4","m4","active",2,"2026-06-15"),
      ("p4", "u10", "m4", "active", 2, "2026-06-15"),
        ("p6", "u5", "m3", "expired", 1, "2026-03-01"),
    ]

    cur.executemany("INSERT OR REPLACE INTO prescriptions VALUES (?,?,?,?,?,?)", prescriptions)

    medications_sold = [
        # ---- 2023 ----
        ("ms1", "m6", "u1", "p1", 30, 1.20, 36.0, "2023-02-15 10:30:00", 2023, 2, 15),
        ("ms2", "m6", "u2", None, 60, 1.10, 66.0, "2023-05-10 14:20:00", 2023, 5, 10),
        ("ms3", "m6", "u4", "p3", 30, 1.20, 36.0, "2023-09-01 09:10:00", 2023, 9, 1),

        # ---- 2024 ----
        ("ms4", "m6", "u1", "p1", 30, 1.25, 37.5, "2024-01-18 11:45:00", 2024, 1, 18),
        ("ms5", "m6", "u5", None, 90, 1.10, 99.0, "2024-03-22 16:00:00", 2024, 3, 22),
        ("ms6", "m6", "u10", "p4", 30, 1.30, 39.0, "2024-07-07 12:30:00", 2024, 7, 7),
        ("ms7", "m6", "u2", "p2", 60, 1.20, 72.0, "2024-11-19 10:15:00", 2024, 11, 19),

        # ---- 2025 ----
        ("ms8", "m6", "u1", "p1", 30, 1.35, 40.5, "2025-01-05 09:00:00", 2025, 1, 5),
        ("ms9", "m6", "u4", None, 60, 1.25, 75.0, "2025-04-12 15:40:00", 2025, 4, 12),
        ("ms10", "m6", "u10", "p4", 30, 1.40, 42.0, "2025-09-03 11:20:00", 2025, 9, 3),
    ]

    cur.executemany(
        """
        INSERT OR REPLACE INTO medications_sold
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """,
        medications_sold
    )

    c.commit()
    c.close()

if __name__ == "__main__":
    seed()
