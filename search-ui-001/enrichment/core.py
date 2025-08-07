#!/usr/bin/env python3
"""
Core enrichment operations and utilities
"""

import logging
from typing import Dict, List, Optional, Tuple
from document_enricher import DocumentEnricher
from keyword_extractor import SmartKeywordExtractor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnrichmentCore:
    """Core enrichment operations"""
    
    def __init__(self, config_path: str = "config.yaml", create_new_index: bool = True):
        """Initialize the enrichment core"""
        self.config_path = config_path
        self.create_new_index = create_new_index
        self.enricher = DocumentEnricher(config_path=config_path, create_new_index=create_new_index)
        self.extractor = SmartKeywordExtractor(config_path=config_path)
    
    def create_enriched_indexes(self, indexes: Optional[List[str]] = None, 
                               batch_size: int = 100, dry_run: bool = False) -> Dict[str, bool]:
        """Create new enriched indexes"""
        logger.info("🚀 Creating enriched indexes")
        
        if dry_run:
            logger.info("🔍 DRY RUN MODE - No changes will be made")
            return self._dry_run_create_indexes(indexes)
        
        results = {}
        indexes_config = self.enricher.config.get('elasticsearch', {}).get('indexes', {})
        
        if indexes:
            # Process specific indexes
            for index_name in indexes:
                enriched_index = indexes_config.get(index_name)
                if not enriched_index:
                    logger.error(f"No enriched index mapping found for {index_name}")
                    results[index_name] = False
                    continue
                
                try:
                    success = self.enricher.process_index(index_name, enriched_index, batch_size)
                    results[index_name] = success
                    if success:
                        logger.info(f"✅ Successfully created enriched index for {index_name}")
                    else:
                        logger.error(f"❌ Failed to create enriched index for {index_name}")
                except Exception as e:
                    logger.error(f"❌ Error processing {index_name}: {e}")
                    results[index_name] = False
        else:
            # Process all indexes
            self.enricher.process_all_indexes()
            results = {index: True for index in indexes_config.keys()}
        
        return results
    
    def update_existing_documents(self, indexes: Optional[List[str]] = None,
                                 batch_size: int = 100, dry_run: bool = False) -> Dict[str, bool]:
        """Update existing documents with enriched fields"""
        logger.info("🔄 Updating existing documents")
        
        if dry_run:
            logger.info("🔍 DRY RUN MODE - No changes will be made")
            return self._dry_run_update_documents(indexes)
        
        results = {}
        indexes_config = self.enricher.config.get('elasticsearch', {}).get('indexes', {})
        
        if indexes:
            # Process specific indexes
            for index_name in indexes:
                try:
                    success = self.enricher.update_existing_documents(index_name, batch_size)
                    results[index_name] = success
                    if success:
                        logger.info(f"✅ Successfully updated documents in {index_name}")
                    else:
                        logger.error(f"❌ Failed to update documents in {index_name}")
                except Exception as e:
                    logger.error(f"❌ Error updating {index_name}: {e}")
                    results[index_name] = False
        else:
            # Process all indexes
            for index_name in indexes_config.keys():
                try:
                    success = self.enricher.update_existing_documents(index_name, batch_size)
                    results[index_name] = success
                except Exception as e:
                    logger.error(f"❌ Error updating {index_name}: {e}")
                    results[index_name] = False
        
        return results
    
    def extract_keywords(self, index: str, output_file: str = "keywords_output.json") -> Dict:
        """Extract keywords from a specific index"""
        logger.info(f"🔍 Extracting keywords from {index}")
        
        try:
            # Extract keywords
            keywords = self.extractor.process_all_indexes()
            
            # Save to file
            self.extractor.save_keywords_library(keywords, output_file)
            
            logger.info(f"✅ Keywords extracted and saved to {output_file}")
            logger.info(f"📊 Total keywords: {len(keywords['technical_terms'])}")
            
            return keywords
        except Exception as e:
            logger.error(f"❌ Error extracting keywords: {e}")
            raise
    
    def get_index_info(self) -> Dict[str, Dict]:
        """Get information about configured indexes"""
        indexes_config = self.enricher.config.get('elasticsearch', {}).get('indexes', {})
        
        info = {
            'source_indexes': list(indexes_config.keys()),
            'enriched_indexes': list(indexes_config.values()),
            'total_indexes': len(indexes_config),
            'mappings': indexes_config
        }
        
        return info
    
    def _dry_run_create_indexes(self, indexes: Optional[List[str]] = None) -> Dict[str, bool]:
        """Dry run for creating indexes"""
        indexes_config = self.enricher.config.get('elasticsearch', {}).get('indexes', {})
        
        if indexes:
            logger.info(f"📋 Would process indexes: {indexes}")
        else:
            logger.info(f"📋 Would process all indexes: {list(indexes_config.keys())}")
        
        logger.info("🔧 Mode: Create new enriched indexes")
        return {index: True for index in (indexes or indexes_config.keys())}
    
    def _dry_run_update_documents(self, indexes: Optional[List[str]] = None) -> Dict[str, bool]:
        """Dry run for updating documents"""
        indexes_config = self.enricher.config.get('elasticsearch', {}).get('indexes', {})
        
        if indexes:
            logger.info(f"📋 Would update indexes: {indexes}")
        else:
            logger.info(f"📋 Would update all indexes: {list(indexes_config.keys())}")
        
        logger.info("🔧 Mode: Update existing documents")
        return {index: True for index in (indexes or indexes_config.keys())}

def create_enrichment_core(config_path: str = "config.yaml", create_new_index: bool = True) -> EnrichmentCore:
    """Factory function to create an enrichment core instance"""
    return EnrichmentCore(config_path=config_path, create_new_index=create_new_index) 