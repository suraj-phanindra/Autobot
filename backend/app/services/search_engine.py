"""Search engine service.

Implements hybrid search combining:
- Semantic vector search via pgvector (cosine similarity)
- Full-text search via PostgreSQL tsvector/tsquery
- Structured field filtering (make, model, year, price, etc.)

Results are fused and re-ranked before being returned.
"""
