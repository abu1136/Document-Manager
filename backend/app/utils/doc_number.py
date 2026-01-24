from sqlalchemy import text
from datetime import datetime

def generate_doc_number(db):
    year = datetime.now().year
    res = db.execute(text("SELECT last_number FROM document_sequence WHERE year=:y"), {"y":year}).fetchone()

    if not res:
        db.execute(text("INSERT INTO document_sequence VALUES (:y,1)"), {"y":year})
        seq = 1
    else:
        seq = res[0] + 1
        db.execute(text("UPDATE document_sequence SET last_number=:s WHERE year=:y"), {"s":seq,"y":year})

    return f"COMP/DOC/{year}/{seq:06d}"
