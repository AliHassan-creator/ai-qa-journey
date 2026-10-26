"""Execute SQL exercises and deterministic data-quality checks in SQLite."""

import re
import sqlite3
from pathlib import Path


FOLDER = Path(__file__).parent


def read_exercises(connection: sqlite3.Connection) -> int:
    """Run the numbered SELECT statements in sql_exercises.sql."""
    source = (FOLDER / "sql_exercises.sql").read_text(encoding="utf-8")
    sections = re.split(r"(?m)^-- Query (\d+): ([^\r\n]+)\r?\n", source)
    query_count = 0

    for index in range(1, len(sections), 3):
        number, title, body = sections[index : index + 3]
        statement = body.split(";", maxsplit=1)[0].strip()
        if not statement:
            raise ValueError(f"Query {number} ({title}) is empty")
        rows = connection.execute(statement).fetchall()
        print(f"Q{number}: {title} -> {len(rows)} row(s)")
        query_count += 1

    return query_count


def verify_data_checks(connection: sqlite3.Connection) -> int:
    """Find five intentionally seeded data-quality issues."""
    checks = [
        (
            "Order total differs from item totals",
            """SELECT o.order_id
               FROM orders AS o
               JOIN order_items AS oi ON oi.order_id = o.order_id
               GROUP BY o.order_id, o.order_total
               HAVING ABS(o.order_total - SUM(oi.quantity * oi.unit_price)) > 0.009
               ORDER BY o.order_id""",
            [(102,)],
        ),
        (
            "Order item references a missing order",
            """SELECT oi.item_id
               FROM order_items AS oi
               LEFT JOIN orders AS o ON o.order_id = oi.order_id
               WHERE o.order_id IS NULL
               ORDER BY oi.item_id""",
            [(908,)],
        ),
        (
            "Duplicate non-null customer email",
            """SELECT email
               FROM customers
               WHERE email IS NOT NULL
               GROUP BY email
               HAVING COUNT(*) > 1""",
            [("asha@example.test",)],
        ),
        (
            "Order has no line items",
            """SELECT o.order_id
               FROM orders AS o
               LEFT JOIN order_items AS oi ON oi.order_id = o.order_id
               WHERE oi.item_id IS NULL
               ORDER BY o.order_id""",
            [(105,)],
        ),
        (
            "Order item has non-positive quantity or negative price",
            """SELECT item_id
               FROM order_items
               WHERE quantity <= 0 OR unit_price < 0
               ORDER BY item_id""",
            [(909,)],
        ),
    ]

    for label, statement, expected_rows in checks:
        actual_rows = connection.execute(statement).fetchall()
        if actual_rows != expected_rows:
            raise AssertionError(
                f"{label}: expected {expected_rows}, found {actual_rows}"
            )
        print(f"EXPECTED ISSUE DETECTED: {label} ({len(actual_rows)})")

    return len(checks)


def main() -> None:
    connection = sqlite3.connect(":memory:")
    try:
        setup_sql = (FOLDER / "sample_orders.sql").read_text(encoding="utf-8")
        connection.executescript(setup_sql)
        query_count = read_exercises(connection)
        check_count = verify_data_checks(connection)

        assert query_count == 12, f"Expected 12 SQL exercises, found {query_count}"
        assert check_count == 5, f"Expected 5 validation checks, found {check_count}"
        print(
            f"\nVerification passed: {query_count} queries executed; "
            f"{check_count} seeded data issues detected as expected."
        )
    finally:
        connection.close()


if __name__ == "__main__":
    main()
