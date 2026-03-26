# Step 3: Database Layer with SQLite and SQLAlchemy

## Overview

This step creates the structured data layer used for numerical analysis.

## Objective

- Build a local SQLite database.
- Create a `sales` table with realistic business fields.
- Seed the table with sample data.

## Components Involved

- `src/create_database.py`
- `data/sales.db`
- SQLite
- SQLAlchemy

## Workflow

1. Define the `sales` table schema.
2. Create the database file.
3. Insert sample rows for sales analytics.

## Commands Used

```bash
python src/create_database.py
```

## Outputs Produced

- `data/sales.db`
- A seeded `sales` table with sample transactions

## Architecture Notes

The database is the structured-data source of truth. The SQL tool queries this layer when the user asks for metrics, rankings, counts, or revenue analysis.

## Troubleshooting Notes

- If `sales.db` is missing, rerun the database script.
- If SQL queries fail with `no such table: sales`, the database was not built correctly.

## Terminology Learned

- Schema
- Table
- Row
- Primary key
- SQLAlchemy engine

## Summary

Step 3 establishes the structured analytics foundation. This is the part of the system best suited for precise business metrics.
