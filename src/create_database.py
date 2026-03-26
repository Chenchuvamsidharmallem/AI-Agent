"""Create and seed the SQLite sales database."""

from __future__ import annotations

import os
from pathlib import Path

from sqlalchemy import (
    Boolean,
    Column,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
)

BASE_DIR = Path(__file__).resolve().parents[1]

metadata = MetaData()

sales_table = Table(
    "sales",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("order_date", String, nullable=False),
    Column("region", String, nullable=False),
    Column("product_name", String, nullable=False),
    Column("category", String, nullable=False),
    Column("sales_rep", String, nullable=False),
    Column("customer_segment", String, nullable=False),
    Column("units_sold", Integer, nullable=False),
    Column("unit_price", Float, nullable=False),
    Column("discount_pct", Float, nullable=False),
    Column("total_revenue", Float, nullable=False),
    Column("returned", Boolean, nullable=False, default=False),
    Column("return_reason", String, nullable=True),
)


SAMPLE_SALES_DATA = [
    {
        "id": 1,
        "order_date": "2025-01-04",
        "region": "North",
        "product_name": "Insight Pro",
        "category": "Analytics",
        "sales_rep": "Avery",
        "customer_segment": "Enterprise",
        "units_sold": 18,
        "unit_price": 1200.0,
        "discount_pct": 0.10,
        "total_revenue": 19440.0,
        "returned": False,
        "return_reason": None,
    },
    {
        "id": 2,
        "order_date": "2025-01-08",
        "region": "West",
        "product_name": "Dashboard Plus",
        "category": "BI",
        "sales_rep": "Jordan",
        "customer_segment": "SMB",
        "units_sold": 34,
        "unit_price": 420.0,
        "discount_pct": 0.05,
        "total_revenue": 13566.0,
        "returned": False,
        "return_reason": None,
    },
    {
        "id": 3,
        "order_date": "2025-01-11",
        "region": "South",
        "product_name": "Forecast AI",
        "category": "Forecasting",
        "sales_rep": "Morgan",
        "customer_segment": "Mid-Market",
        "units_sold": 16,
        "unit_price": 950.0,
        "discount_pct": 0.08,
        "total_revenue": 13984.0,
        "returned": False,
        "return_reason": None,
    },
    {
        "id": 4,
        "order_date": "2025-01-15",
        "region": "East",
        "product_name": "Insight Lite",
        "category": "Analytics",
        "sales_rep": "Taylor",
        "customer_segment": "SMB",
        "units_sold": 42,
        "unit_price": 260.0,
        "discount_pct": 0.03,
        "total_revenue": 10592.4,
        "returned": True,
        "return_reason": "Customer switched to a competitor",
    },
    {
        "id": 5,
        "order_date": "2025-01-19",
        "region": "North",
        "product_name": "Forecast AI",
        "category": "Forecasting",
        "sales_rep": "Avery",
        "customer_segment": "Enterprise",
        "units_sold": 12,
        "unit_price": 950.0,
        "discount_pct": 0.12,
        "total_revenue": 10032.0,
        "returned": False,
        "return_reason": None,
    },
    {
        "id": 6,
        "order_date": "2025-01-24",
        "region": "West",
        "product_name": "Insight Pro",
        "category": "Analytics",
        "sales_rep": "Jordan",
        "customer_segment": "Mid-Market",
        "units_sold": 14,
        "unit_price": 1200.0,
        "discount_pct": 0.07,
        "total_revenue": 15624.0,
        "returned": False,
        "return_reason": None,
    },
    {
        "id": 7,
        "order_date": "2025-02-02",
        "region": "South",
        "product_name": "Dashboard Plus",
        "category": "BI",
        "sales_rep": "Morgan",
        "customer_segment": "SMB",
        "units_sold": 38,
        "unit_price": 420.0,
        "discount_pct": 0.04,
        "total_revenue": 15321.6,
        "returned": True,
        "return_reason": "Integration setup confusion",
    },
    {
        "id": 8,
        "order_date": "2025-02-07",
        "region": "East",
        "product_name": "Forecast AI",
        "category": "Forecasting",
        "sales_rep": "Taylor",
        "customer_segment": "Enterprise",
        "units_sold": 20,
        "unit_price": 950.0,
        "discount_pct": 0.09,
        "total_revenue": 17290.0,
        "returned": False,
        "return_reason": None,
    },
    {
        "id": 9,
        "order_date": "2025-02-10",
        "region": "North",
        "product_name": "Dashboard Plus",
        "category": "BI",
        "sales_rep": "Avery",
        "customer_segment": "SMB",
        "units_sold": 30,
        "unit_price": 420.0,
        "discount_pct": 0.02,
        "total_revenue": 12348.0,
        "returned": False,
        "return_reason": None,
    },
    {
        "id": 10,
        "order_date": "2025-02-14",
        "region": "West",
        "product_name": "Insight Lite",
        "category": "Analytics",
        "sales_rep": "Jordan",
        "customer_segment": "SMB",
        "units_sold": 45,
        "unit_price": 260.0,
        "discount_pct": 0.03,
        "total_revenue": 11349.0,
        "returned": False,
        "return_reason": None,
    },
    {
        "id": 11,
        "order_date": "2025-02-18",
        "region": "South",
        "product_name": "Insight Pro",
        "category": "Analytics",
        "sales_rep": "Morgan",
        "customer_segment": "Enterprise",
        "units_sold": 15,
        "unit_price": 1200.0,
        "discount_pct": 0.11,
        "total_revenue": 16020.0,
        "returned": False,
        "return_reason": None,
    },
    {
        "id": 12,
        "order_date": "2025-02-27",
        "region": "East",
        "product_name": "Dashboard Plus",
        "category": "BI",
        "sales_rep": "Taylor",
        "customer_segment": "Mid-Market",
        "units_sold": 28,
        "unit_price": 420.0,
        "discount_pct": 0.06,
        "total_revenue": 11054.4,
        "returned": False,
        "return_reason": None,
    },
    {
        "id": 13,
        "order_date": "2025-03-03",
        "region": "North",
        "product_name": "Insight Lite",
        "category": "Analytics",
        "sales_rep": "Avery",
        "customer_segment": "SMB",
        "units_sold": 50,
        "unit_price": 260.0,
        "discount_pct": 0.04,
        "total_revenue": 12480.0,
        "returned": False,
        "return_reason": None,
    },
    {
        "id": 14,
        "order_date": "2025-03-08",
        "region": "West",
        "product_name": "Forecast AI",
        "category": "Forecasting",
        "sales_rep": "Jordan",
        "customer_segment": "Enterprise",
        "units_sold": 17,
        "unit_price": 950.0,
        "discount_pct": 0.10,
        "total_revenue": 14535.0,
        "returned": False,
        "return_reason": None,
    },
    {
        "id": 15,
        "order_date": "2025-03-11",
        "region": "South",
        "product_name": "Insight Lite",
        "category": "Analytics",
        "sales_rep": "Morgan",
        "customer_segment": "SMB",
        "units_sold": 39,
        "unit_price": 260.0,
        "discount_pct": 0.05,
        "total_revenue": 9633.0,
        "returned": True,
        "return_reason": "Requested premium reporting features",
    },
    {
        "id": 16,
        "order_date": "2025-03-14",
        "region": "East",
        "product_name": "Insight Pro",
        "category": "Analytics",
        "sales_rep": "Taylor",
        "customer_segment": "Mid-Market",
        "units_sold": 13,
        "unit_price": 1200.0,
        "discount_pct": 0.07,
        "total_revenue": 14508.0,
        "returned": False,
        "return_reason": None,
    },
    {
        "id": 17,
        "order_date": "2025-03-19",
        "region": "North",
        "product_name": "Forecast AI",
        "category": "Forecasting",
        "sales_rep": "Avery",
        "customer_segment": "Mid-Market",
        "units_sold": 19,
        "unit_price": 950.0,
        "discount_pct": 0.08,
        "total_revenue": 16606.0,
        "returned": False,
        "return_reason": None,
    },
    {
        "id": 18,
        "order_date": "2025-03-25",
        "region": "West",
        "product_name": "Dashboard Plus",
        "category": "BI",
        "sales_rep": "Jordan",
        "customer_segment": "Enterprise",
        "units_sold": 24,
        "unit_price": 420.0,
        "discount_pct": 0.08,
        "total_revenue": 9273.6,
        "returned": False,
        "return_reason": None,
    },
]


def resolve_database_path() -> Path:
    """Return the database file path, supporting Azure-style absolute SQLite URLs."""
    raw_url = os.getenv("DATABASE_URL")
    if not raw_url:
        return BASE_DIR / "data" / "sales.db"

    if not raw_url.startswith("sqlite:///"):
        raise ValueError("This project currently supports only SQLite DATABASE_URL values.")

    raw_path = raw_url.removeprefix("sqlite:///")
    path = Path(raw_path)
    return path if path.is_absolute() else BASE_DIR / path


def create_database(*, overwrite: bool = True) -> Path:
    """Create the SQLite database and populate it with sample records."""
    database_path = resolve_database_path()
    database_path.parent.mkdir(parents=True, exist_ok=True)

    if database_path.exists():
        if not overwrite:
            print(f"Database already exists at: {database_path}")
            return database_path
        database_path.unlink()

    engine = create_engine(f"sqlite:///{database_path}")
    metadata.create_all(engine)

    with engine.begin() as connection:
        connection.execute(sales_table.insert(), SAMPLE_SALES_DATA)

    print(f"Database created at: {database_path}")
    print(f"Inserted {len(SAMPLE_SALES_DATA)} rows into the sales table.")
    return database_path


if __name__ == "__main__":
    create_database()
