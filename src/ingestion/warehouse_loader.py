"""Warehouse loader command."""

from src.storage.duckdb_store import load_duckdb_store


def main() -> str:
    """Load DuckDB warehouse."""
    return load_duckdb_store()


if __name__ == "__main__":
    main()

