"""RAG (Retrieval-Augmented Generation) pipeline service.

Orchestrates the full search-to-answer flow:
1. Query understanding and intent extraction (LLM)
2. Hybrid search via search_engine
3. Context assembly from retrieved chunks and vehicle data
4. Answer generation with citations (LLM)
5. Search logging and analytics
"""
