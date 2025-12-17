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

    c.commit()
    c.close()

if __name__ == "__main__":
    seed()
