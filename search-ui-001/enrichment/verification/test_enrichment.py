#!/usr/bin/env python3
"""
Non-interactive test script for the enrichment process
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from document_enricher import DocumentEnricher
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_enrichment():
    """Test the enrichment process"""
    print("🧪 Testing Enrichment Process")
    print("=" * 50)
    print()
    
    try:
        # Initialize enricher with create_new_index=True
        enricher = DocumentEnricher(create_new_index=True)
        
        # Process all indexes
        enricher.process_all_indexes()
        
        print("\n✅ Enrichment test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during enrichment test: {e}")
        logger.error(f"Error during enrichment test: {e}")
        raise

if __name__ == "__main__":
    test_enrichment() 