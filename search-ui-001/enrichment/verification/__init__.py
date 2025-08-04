"""
Verification Module for Document Enrichment

This module contains all verification and testing scripts for the enrichment framework.
"""

from .verify_enriched_fields import verify_enriched_fields, check_index_stats
from .detailed_verification import examine_document_content
from .check_original_content import examine_original_documents
from .test_fixed_extraction import test_keyword_extraction
from .test_enriched_config import test_enriched_indexes
from .final_verification_summary import generate_final_summary
from .test_content_paths import test_content_paths
from .test_backend_enriched import test_backend_with_enriched_indexes

__version__ = "1.0.0"
__author__ = "Elastic Search Team"

__all__ = [
    'verify_enriched_fields',
    'check_index_stats',
    'examine_document_content',
    'examine_original_documents',
    'test_keyword_extraction',
    'test_enriched_indexes',
    'generate_final_summary',
    'test_content_paths',
    'test_backend_with_enriched_indexes'
] 