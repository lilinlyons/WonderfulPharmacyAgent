from backend.workflows.db_tools.db import conn, init_schema

def seed():
    init_schema()
    c = conn()
    cur = c.cursor()

    users = [
      ("u1","Or Levi","050-1111111","he"),
      ("u2","Dana Cohen","050-2222222","he"),
      ("u3","Noam David","050-3333333","he"),
      ("u4","Maya Katz","050-4444444","en"),
      ("u5","Eitan Bar","050-5555555","he"),
      ("u6","Yael Azulay","050-6666666","he"),
      ("u7","Tom Green","050-7777777","en"),
      ("u8","Shira Malka","050-8888888","he"),
      ("u9","Avi Ron","050-9999999","he"),
      ("u10","Liam Stone","050-1010101","en"),
    ]
    cur.executemany("INSERT OR REPLACE INTO users VALUES (?,?,?,?)", users)

    meds = [
      ("m1","Acamol","Paracetamol","Paracetamol",0,"Tablet","500mg",
       "Adults: follow package directions. Do not exceed the maximum daily dose on label.",
       "מבוגרים: לפעול לפי הוראות העלון. אין לעבור את המינון היומי המרבי בעלון.",
       "Do not use with other products containing paracetamol. Seek help if overdose suspected.",
       "אין לשלב עם מוצרים נוספים המכילים פראצטמול. במקרה חשד למינון יתר לפנות לעזרה רפואית."),
      ("m2","Nurofen","Ibuprofen","Ibuprofen",0,"Capsule","200mg",
       "Take with food/water as directed on label. Do not exceed label maximum.",
       "יש ליטול עם אוכל/מים לפי העלון. אין לעבור את המינון המרבי בעלון.",
       "May not be suitable with certain conditions/meds—ask a pharmacist/doctor.",
       "ייתכן שאינו מתאים במצבים/תרופות מסוימים—יש להתייעץ עם רוקח/רופא."),
      ("m3","Augmentin","Amoxicillin/Clavulanate","Amoxicillin + Clavulanate",1,"Tablet","875/125mg",
       "Prescription-only antibiotic. Use exactly as prescribed; complete the course.",
       "אנטיביוטיקה במרשם. להשתמש בדיוק לפי מרשם; להשלים את הטיפול.",
       "Allergy risk (penicillins). Seek urgent help for severe allergic reaction signs.",
       "סיכון לאלרגיה (פניצילינים). במקרה תסמינים חמורים לפנות בדחיפות."),
      ("m4","Ventolin","Salbutamol","Salbutamol",1,"Inhaler","100mcg/dose",
       "Prescription-only. Use exactly as prescribed. Refer to device instructions.",
       "במרשם. להשתמש בדיוק לפי מרשם. לעיין בהוראות השימוש במשאף.",
       "If breathing worsens or relief is inadequate, seek urgent medical help.",
       "אם יש החמרה בנשימה או שאין הקלה מספקת—לפנות בדחיפות."),
      ("m5","Claritin","Loratadine","Loratadine",0,"Tablet","10mg",
       "Once daily as directed on label.",
       "פעם ביום לפי העלון.",
       "May cause drowsiness in some people. Check label warnings.",
       "עלול לגרום לישנוניות אצל חלק מהאנשים. לעיין באזהרות בעלון."),
    ]
    cur.executemany("INSERT OR REPLACE INTO medications VALUES (?,?,?,?,?,?,?,?,?,?,?)", meds)

    stock_rows = [
      ("store_tlv","m1",42),("store_tlv","m2",15),("store_tlv","m3",5),("store_tlv","m4",0),("store_tlv","m5",18),
      ("store_jlm","m1",10),("store_jlm","m2",0),("store_jlm","m3",2),("store_jlm","m4",7),("store_jlm","m5",4),
    ]
    cur.executemany("INSERT OR REPLACE INTO stock VALUES (?,?,?)", stock_rows)

    prescriptions = [
      ("p1","u1","m3","active",1,"2026-03-01"),
      ("p2","u1","m4","expired",0,"2025-10-10"),
      ("p3","u4","m4","active",2,"2026-06-15"),
    ]
    cur.executemany("INSERT OR REPLACE INTO prescriptions VALUES (?,?,?,?,?,?)", prescriptions)

    c.commit()
    c.close()

if __name__ == "__main__":
    seed()
