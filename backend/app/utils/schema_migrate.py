from sqlalchemy import text
from sqlalchemy.engine import Engine


def ensure_column(engine: Engine, table: str, column: str, ddl: str):
    """
    Ensure a column exists, otherwise add it.
    ddl example: "ALTER TABLE documents ADD COLUMN pdf_path VARCHAR(255)"
    """
    with engine.connect() as conn:
        res = conn.execute(
            text("""
            SELECT COUNT(*) AS cnt
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = :table
              AND COLUMN_NAME = :column
            """),
            {"table": table, "column": column},
        )
        exists = res.scalar()

        if not exists:
            conn.execute(text(ddl))
            conn.commit()
