"""Embedding service.

Generates vector embeddings for document chunks and search queries
using OpenAI's text-embedding-3-small model (1536 dimensions).
Handles batching and retry logic for the embedding API.
"""
