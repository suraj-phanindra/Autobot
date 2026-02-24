"""CSV importer service.

Handles bulk vehicle import from CSV files. Supports column mapping,
validation, deduplication by VIN, and batch upsert into the vehicles table.
Provides progress tracking and error reporting for large imports.
"""
