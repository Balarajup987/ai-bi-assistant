
import pandas as pd
from app.database import get_connection, create_table
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "sales1.csv"


def load_sales_data():
    print("Reading CSV file...")

    df = pd.read_csv(CSV_PATH)

    # Convert date and numeric columns
    df["Order_date"] = pd.to_datetime(
        df["Order_date"], format="%d-%m-%Y", errors="coerce"
    )

    numeric_columns = ["Quantity", "Unit_price", "Discount_amount"]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Create database table
    create_table()

    conn = get_connection()
    loaded = 0
    skipped = 0

    for _, row in df.iterrows():

        required = [
            "Transaction_Id", "Product", "Category",
            "Region", "Sales_channel", "Status"
        ]

        if any(pd.isna(row[col]) for col in required):
            skipped += 1
            continue

        if pd.isna(row["Order_date"]):
            skipped += 1
            continue

        issues = []

        if pd.isna(row["Unit_price"]):
            issues.append("Missing unit price")

        if pd.isna(row["Quantity"]):
            issues.append("Missing quantity")
        elif row["Quantity"] <= 0:
            issues.append("Invalid quantity")

        if pd.isna(row["Discount_amount"]):
            issues.append("Missing discount")
        elif row["Discount_amount"] < 0:
            issues.append("Invalid discount")

        if not pd.isna(row["Unit_price"]) and row["Unit_price"] < 0:
            issues.append("Invalid unit price")

        if (
            not pd.isna(row["Quantity"])
            and not pd.isna(row["Unit_price"])
            and not pd.isna(row["Discount_amount"])
        ):
            gross = row["Quantity"] * row["Unit_price"]
            if row["Discount_amount"] > gross:
                issues.append("Discount exceeds gross sales")

        record = (
            str(row["Transaction_Id"]),
            row["Order_date"].strftime("%Y-%m-%d"),
            str(row["Product"]),
            str(row["Category"]),
            str(row["Region"]),
            str(row["Sales_channel"]),
            None if pd.isna(row["Quantity"]) else int(row["Quantity"]),
            None if pd.isna(row["Unit_price"]) else float(row["Unit_price"]),
            None if pd.isna(row["Discount_amount"]) else float(row["Discount_amount"]),
            str(row["Status"]),
            ", ".join(issues) if issues else None
        )

        conn.execute("""
            INSERT OR REPLACE INTO sales VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """, record)

        loaded += 1

    conn.commit()
    conn.close()

    return {
        "total_records": len(df),
        "loaded_records": loaded,
        "skipped_records": skipped
    }


if __name__ == "__main__":
    result = load_sales_data()
    print("Data loading completed!")
    print(result)
