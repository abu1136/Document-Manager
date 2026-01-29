from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime

from app.models.document import Document


PREFIX = "COMP/DOC"


def generate_doc_number(db: Session) -> str:
    """
    Generates document number in format:
    COMP/DOC/YYYY/000001

    - Increments safely
    - Resets every year
    """

    year = datetime.now().year

    # Get last document for current year
    last_doc = (
        db.query(Document)
        .filter(Document.document_number.like(f"{PREFIX}/{year}/%"))
        .order_by(desc(Document.document_number))
        .first()
    )

    if not last_doc:
        next_number = 1
    else:
        try:
            last_seq = int(last_doc.document_number.split("/")[-1])
            next_number = last_seq + 1
        except Exception:
            next_number = 1

    return f"{PREFIX}/{year}/{next_number:06d}"
