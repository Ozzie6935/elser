"""
Isolated Document Enrichment Framework

This is a completely self-contained enrichment framework that can be used independently.
It provides functionality to enrich Elasticsearch documents with:
- Keyword extraction
- Entity recognition
- URL metadata extraction
- Technical term identification
- Content analysis

Main components:
- SmartKeywordExtractor: Extracts intelligent keywords from documents
- DocumentEnricher: Enriches documents with extracted metadata
- Verification module: Comprehensive testing and verification scripts
"""

from .keyword_extractor import SmartKeywordExtractor
from .document_enricher import DocumentEnricher

# Import verification functions
from .verification import (
    verify_enriched_fields,
    check_index_stats,
    examine_document_content,
    examine_original_documents,
    test_keyword_extraction,
    test_enriched_indexes,
    generate_final_summary
)

__version__ = "1.0.0"
__author__ = "Elastic Search Team"

__all__ = [
    'SmartKeywordExtractor',
    'DocumentEnricher',
    'verify_enriched_fields',
    'check_index_stats',
    'examine_document_content',
    'examine_original_documents',
    'test_keyword_extraction',
    'test_enriched_indexes',
    'generate_final_summary'
] 