
from app.database import get_connection


def get_total_revenue():
    conn = get_connection()

    result = conn.execute("""
        SELECT SUM(quantity * unit_price - discount_amount)
        FROM sales
        WHERE status = 'Completed'
          AND quantity > 0
          AND unit_price IS NOT NULL
          AND unit_price >= 0
          AND discount_amount IS NOT NULL
          AND discount_amount >= 0
          AND discount_amount <= quantity * unit_price
    """).fetchone()

    conn.close()
    return result[0] or 0


def get_top_product():
    conn = get_connection()

    result = conn.execute("""
        SELECT product,
               SUM(quantity * unit_price - discount_amount) AS revenue
        FROM sales
        WHERE status = 'Completed'
          AND quantity > 0
          AND unit_price IS NOT NULL
          AND unit_price >= 0
          AND discount_amount IS NOT NULL
          AND discount_amount >= 0
          AND discount_amount <= quantity * unit_price
        GROUP BY product
        ORDER BY revenue DESC
        LIMIT 1
    """).fetchone()

    conn.close()

    return dict(result) if result else None


def get_region_sales():
    conn = get_connection()

    results = conn.execute("""
        SELECT region,
               SUM(quantity * unit_price - discount_amount) AS revenue
        FROM sales
        WHERE status = 'Completed'
          AND quantity > 0
          AND unit_price IS NOT NULL
          AND unit_price >= 0
          AND discount_amount IS NOT NULL
          AND discount_amount >= 0
          AND discount_amount <= quantity * unit_price
        GROUP BY region
        ORDER BY revenue DESC
    """).fetchall()

    conn.close()
    return [dict(row) for row in results]


def get_monthly_sales():
    conn = get_connection()

    results = conn.execute("""
        SELECT strftime('%Y-%m', order_date) AS month,
               SUM(quantity * unit_price - discount_amount) AS revenue
        FROM sales
        WHERE status = 'Completed'
          AND quantity > 0
          AND unit_price IS NOT NULL
          AND unit_price >= 0
          AND discount_amount IS NOT NULL
          AND discount_amount >= 0
          AND discount_amount <= quantity * unit_price
        GROUP BY month
        ORDER BY month
    """).fetchall()

    conn.close()
    return [dict(row) for row in results]

def analyze_sales(
    metric="revenue",
    group_by=None,
    filters=None,
    sort="desc",
    limit=None
):
    conn = get_connection()

    # Only allow predefined database columns.
    allowed_dimensions = {
        "region": "region",
        "product": "product",
        "category": "category",
        "sales_channel": "sales_channel",
        "month": "SUBSTR(order_date, 1, 7)"
    }

    allowed_metrics = {
        "revenue": "SUM(quantity * unit_price - discount_amount)",
        "quantity": "SUM(quantity)",
        "transactions": "COUNT(*)"
    }

    if metric not in allowed_metrics:
        conn.close()
        raise ValueError("Unsupported metric")

    if group_by and group_by not in allowed_dimensions:
        conn.close()
        raise ValueError("Unsupported grouping")

    filters = filters or {}

    allowed_filters = {
        "region": "region",
        "product": "product",
        "category": "category",
        "sales_channel": "sales_channel",
        "month": "SUBSTR(order_date, 1, 7)"
    }

    conditions = [
        "status = 'Completed'",
        "quantity > 0",
        "unit_price IS NOT NULL",
        "unit_price >= 0",
        "discount_amount IS NOT NULL",
        "discount_amount >= 0",
        "discount_amount <= quantity * unit_price"
    ]

    params = []

    for key, value in filters.items():
        if value is None:
            continue

        if key not in allowed_filters:
            conn.close()
            raise ValueError("Unsupported filter")

        conditions.append(f"{allowed_filters[key]} = ?")
        params.append(value)

    metric_sql = allowed_metrics[metric]

    if group_by:
        dimension_sql = allowed_dimensions[group_by]

        query = f"""
            SELECT
                {dimension_sql} AS label,
                {metric_sql} AS value
            FROM sales
            WHERE {" AND ".join(conditions)}
            GROUP BY {dimension_sql}
        """

        if sort not in ("asc", "desc"):
            conn.close()
            raise ValueError("Invalid sort order")

        query += f" ORDER BY value {sort.upper()}"

        if limit is not None:
            if not isinstance(limit, int) or limit < 1 or limit > 50:
                conn.close()
                raise ValueError("Invalid limit")
            query += " LIMIT ?"
            params.append(limit)

        rows = conn.execute(query, params).fetchall()
        result = [dict(row) for row in rows]

    else:
        query = f"""
            SELECT {metric_sql} AS value
            FROM sales
            WHERE {" AND ".join(conditions)}
        """

        row = conn.execute(query, params).fetchone()
        result = row["value"] if row else 0

    conn.close()
    return result

def analyze_sales(
    metric="revenue",
    group_by=None,
    filters=None,
    sort="desc",
    limit=None
):
    conn = get_connection()

    allowed_dimensions = {
        "region": "region",
        "product": "product",
        "category": "category",
        "sales_channel": "sales_channel",
        "month": "SUBSTR(order_date, 1, 7)"
    }

    allowed_metrics = {
        "revenue": "SUM(quantity * unit_price - discount_amount)",
        "quantity": "SUM(quantity)",
        "transactions": "COUNT(*)"
    }

    # Validate metric
    if metric not in allowed_metrics:
        conn.close()
        raise ValueError("Unsupported metric")

    # Validate grouping
    if group_by is not None and group_by not in allowed_dimensions:
        conn.close()
        raise ValueError("Unsupported grouping")

    filters = filters or {}

    allowed_filters = {
        "region": "region",
        "product": "product",
        "category": "category",
        "sales_channel": "sales_channel",
        "month": "SUBSTR(order_date, 1, 7)"
    }

    conditions = [
        "status = 'Completed'",
        "quantity > 0",
        "unit_price IS NOT NULL",
        "unit_price >= 0",
        "discount_amount IS NOT NULL",
        "discount_amount >= 0",
        "discount_amount <= quantity * unit_price"
    ]

    params = []

    # Apply filters safely
    for key, value in filters.items():
        if key not in allowed_filters:
            conn.close()
            raise ValueError("Unsupported filter")

        if value is not None:
            conditions.append(f"{allowed_filters[key]} = ?")
            params.append(value)

    metric_sql = allowed_metrics[metric]

    if group_by:
        dimension_sql = allowed_dimensions[group_by]

        query = f"""
            SELECT
                {dimension_sql} AS label,
                {metric_sql} AS value
            FROM sales
            WHERE {" AND ".join(conditions)}
            GROUP BY {dimension_sql}
        """

        if sort not in ("asc", "desc"):
            conn.close()
            raise ValueError("Invalid sort order")

        query += f" ORDER BY value {sort.upper()}"

        if limit is not None:
            if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1 or limit > 50:
                conn.close()
                raise ValueError("Invalid limit")

            query += " LIMIT ?"
            params.append(limit)

        rows = conn.execute(query, params).fetchall()
        result = [dict(row) for row in rows]

    else:
        if limit is not None:
            conn.close()
            raise ValueError("Limit requires a grouping")

        query = f"""
            SELECT {metric_sql} AS value
            FROM sales
            WHERE {" AND ".join(conditions)}
        """

        row = conn.execute(query, params).fetchone()
        result = row["value"] if row else 0

    conn.close()
    return result
def compare_months(month1, month2):
    conn = get_connection()

    query = """
        SELECT
            SUBSTR(order_date, 1, 7) AS month,
            SUM(quantity * unit_price - discount_amount) AS revenue
        FROM sales
        WHERE status = 'Completed'
          AND quantity > 0
          AND unit_price IS NOT NULL
          AND unit_price >= 0
          AND discount_amount IS NOT NULL
          AND discount_amount >= 0
          AND discount_amount <= quantity * unit_price
          AND SUBSTR(order_date, 1, 7) IN (?, ?)
        GROUP BY SUBSTR(order_date, 1, 7)
    """

    rows = conn.execute(query, (month1, month2)).fetchall()
    conn.close()

    results = {row["month"]: row["revenue"] for row in rows}

    revenue1 = results.get(month1, 0)
    revenue2 = results.get(month2, 0)

    difference = revenue2 - revenue1

    if revenue1 == 0:
        percentage_change = None
    else:
        percentage_change = (difference / revenue1) * 100

    return {
        "month1": month1,
        "revenue1": revenue1,
        "month2": month2,
        "revenue2": revenue2,
        "difference": difference,
        "percentage_change": percentage_change,
        "change": (
            "increase" if difference > 0
            else "decrease" if difference < 0
            else "no change"
        )
    }