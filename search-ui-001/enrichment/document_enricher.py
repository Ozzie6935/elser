#!/usr/bin/env python3
"""
Document Enricher - Updates existing documents with extracted keywords
Can either update existing documents or create a new enriched index
"""

import json
import requests
import yaml
from typing import Dict, List, Optional
import logging
from urllib.parse import urlparse
from keyword_extractor import SmartKeywordExtractor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DocumentEnricher:
    def __init__(self, config_path: str = "config.yaml", create_new_index: bool = False):
        """Initialize the document enricher"""
        self.config = self._load_config(config_path)
        self.es_url = self.config['elasticsearch']['host']
        self.api_key = self.config['common']['api_key']
        self.create_new_index = create_new_index
        
        # Initialize keyword extractor
        self.keyword_extractor = SmartKeywordExtractor(config_path)
        
        # New index suffix if creating new index
        self.new_index_suffix = "_enriched"
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.error(f"Config file {config_path} not found")
            raise
    
    def create_enriched_index(self, original_index: str, enriched_index: str = None) -> str:
        """Create a new enriched index with updated mapping"""
        if enriched_index:
            new_index = enriched_index
        else:
            new_index = f"{original_index}{self.new_index_suffix}"

        # Check if index already exists and delete it
        url = f"{self.es_url}/{new_index}"
        try:
            response = requests.head(url, verify=False)
            if response.status_code == 200:
                logger.info(f"Index {new_index} already exists. Deleting it...")
                delete_response = requests.delete(url, verify=False)
                if delete_response.status_code != 200:
                    logger.error(f"Failed to delete existing index {new_index}")
                    return None
                logger.info(f"✅ Deleted existing index {new_index}")
        except requests.exceptions.RequestException as e:
            logger.debug(f"Index {new_index} does not exist or error checking: {e}")

        # Create simplified mapping with keyword fields
        enriched_mapping = self._add_keyword_fields_to_mapping({})

        # Create new index
        headers = {"Content-Type": "application/json"}

        # Debug: Print the JSON being sent
        mapping_json = json.dumps(enriched_mapping, indent=2)
        logger.info(f"Creating index {new_index} with mapping:")
        logger.info(mapping_json)

        try:
            response = requests.put(url, headers=headers, json=enriched_mapping, verify=False)
            response.raise_for_status()
            logger.info(f"✅ Created enriched index: {new_index}")
            return new_index
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to create enriched index {new_index}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response content: {e.response.text}")
            return None
    
    def _get_index_mapping(self, index_name: str) -> Optional[Dict]:
        """Get the mapping for an existing index"""
        url = f"{self.es_url}/{index_name}/_mapping"
        headers = {"Content-Type": "application/json"}
        # No params
        try:
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            data = response.json()
            return data.get(index_name, {}).get('mappings', {})
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting mapping for {index_name}: {e}")
            return None
    
    def _add_keyword_fields_to_mapping(self, original_mapping: Dict) -> Dict:
        """Add keyword fields to existing mapping"""
        # Create a simplified mapping that includes our keyword fields
        # without conflicting with the complex existing structure
        enriched_mapping = {
            "mappings": {
                "properties": {
                    # Keep essential fields from original mapping
                    "content": {
                        "properties": {
                            "body": {
                                "properties": {
                                    "clean_content": {"type": "text"},
                                    "raw_html": {"type": "text"}
                                }
                            }
                        }
                    },
                    "url": {
                        "properties": {
                            "raw": {"type": "text"}
                        }
                    },
                    "title": {
                        "properties": {
                            "raw": {"type": "text"}
                        }
                    },
                    "description": {
                        "properties": {
                            "raw": {"type": "text"}
                        }
                    },
                    "meta": {
                        "properties": {
                            "title": {"type": "text"},
                            "description": {"type": "text"}
                        }
                    },
                    "platform": {"type": "keyword"},
                    "region": {"type": "keyword"},
                    "category": {"type": "keyword"},
                    
                    # New keyword fields for aggregations
                    "programming_language": {
                        "type": "keyword",
                        "fields": {
                            "text": {"type": "text"}
                        }
                    },
                    "framework": {
                        "type": "keyword",
                        "fields": {
                            "text": {"type": "text"}
                        }
                    },
                    "tool": {
                        "type": "keyword",
                        "fields": {
                            "text": {"type": "text"}
                        }
                    },
                    "concept": {
                        "type": "keyword",
                        "fields": {
                            "text": {"type": "text"}
                        }
                    },
                    "content_type": {
                        "type": "keyword",
                        "fields": {
                            "text": {"type": "text"}
                        }
                    },
                    "domain": {
                        "type": "keyword",
                        "fields": {
                            "text": {"type": "text"}
                        }
                    },
                    "technical_terms": {
                        "type": "keyword",
                        "fields": {
                            "text": {"type": "text"}
                        }
                    },
                    "entities": {
                        "properties": {
                            "person": {
                                "type": "keyword",
                                "fields": {
                                    "text": {"type": "text"}
                                }
                            },
                            "organization": {
                                "type": "keyword",
                                "fields": {
                                    "text": {"type": "text"}
                                }
                            },
                            "location": {
                                "type": "keyword",
                                "fields": {
                                    "text": {"type": "text"}
                                }
                            },
                            "gpe": {
                                "type": "keyword",
                                "fields": {
                                    "text": {"type": "text"}
                                }
                            },
                            "product": {
                                "type": "keyword",
                                "fields": {
                                    "text": {"type": "text"}
                                }
                            },
                            "event": {
                                "type": "keyword",
                                "fields": {
                                    "text": {"type": "text"}
                                }
                            }
                        }
                    },
                    "content_length": {
                        "type": "keyword",
                        "fields": {
                            "text": {"type": "text"}
                        }
                    },
                    "language": {
                        "type": "keyword",
                        "fields": {
                            "text": {"type": "text"}
                        }
                    }
                }
            }
        }

        return enriched_mapping
    
    def enrich_document(self, doc: Dict) -> Dict:
        """Enrich a single document with extracted keywords"""
        # Extract keywords using the keyword extractor
        doc_keywords = self.keyword_extractor.extract_keywords_from_document(doc)
        
        # Create enriched document
        enriched_doc = doc.copy()
        
        # Add extracted keywords
        enriched_doc['programming_language'] = list(doc_keywords['programming_languages'])
        enriched_doc['framework'] = list(doc_keywords['frameworks'])
        enriched_doc['tool'] = list(doc_keywords['tools'])
        enriched_doc['concept'] = list(doc_keywords['concepts'])
        enriched_doc['technical_terms'] = list(doc_keywords['technical_terms'])
        
        # Add URL metadata
        url_metadata = doc_keywords.get('url_metadata', {})
        enriched_doc['content_type'] = url_metadata.get('content_type', 'other')
        enriched_doc['domain'] = url_metadata.get('domain', 'unknown')
        
        # Add entities
        enriched_doc['entities'] = {
            entity_type: list(entity_set) 
            for entity_type, entity_set in doc_keywords['entities'].items()
        }
        
        # Add content length categorization
        content_length = len(doc.get('content', ''))
        if content_length < 1000:
            enriched_doc['content_length'] = 'short'
        elif content_length < 5000:
            enriched_doc['content_length'] = 'medium'
        else:
            enriched_doc['content_length'] = 'long'
        
        # Add language (assuming English for now)
        enriched_doc['language'] = 'en'
        
        return enriched_doc
    
    def process_index(self, source_index: str, enriched_index: str = None, batch_size: int = 100):
        """Process all documents in an index and enrich them"""
        logger.info(f"🔄 Processing index: {source_index}")
        
        # Determine target index
        if self.create_new_index:
            if enriched_index:
                target_index = self.create_enriched_index(source_index, enriched_index)
            else:
                target_index = self.create_enriched_index(source_index)
            if not target_index:
                logger.error(f"Failed to create enriched index for {source_index}")
                return False
        else:
            target_index = source_index
        
        # Extract all documents
        documents = self.keyword_extractor.extract_documents_from_index(source_index, batch_size)
        logger.info(f"📄 Found {len(documents)} documents in {source_index}")
        
        # Process documents in batches
        success_count = 0
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            enriched_batch = []
            
            # Enrich each document in the batch
            for doc in batch:
                try:
                    enriched_doc = self.enrich_document(doc)
                    enriched_batch.append({
                        'id': doc['id'],
                        'enriched_doc': enriched_doc
                    })
                except Exception as e:
                    logger.warning(f"Error enriching document {doc.get('id', 'unknown')}: {e}")
            
            # Bulk index enriched documents
            if enriched_batch:
                success = self._bulk_index_documents(target_index, enriched_batch)
                if success:
                    success_count += len(enriched_batch)
                    logger.info(f"✅ Indexed {len(enriched_batch)} enriched documents")
                else:
                    logger.error(f"❌ Failed to index batch of {len(enriched_batch)} documents")
        
        logger.info(f"🎉 Successfully processed {success_count}/{len(documents)} documents for {source_index}")
        return success_count == len(documents)
    
    def _bulk_index_documents(self, index_name: str, documents: List[Dict]) -> bool:
        """Bulk index documents to Elasticsearch"""
        if not documents:
            return True
        
        # Prepare bulk request
        bulk_data = []
        for doc_info in documents:
            # Add index action
            bulk_data.append({
                "index": {
                    "_index": index_name,
                    "_id": doc_info['id']
                }
            })
            # Add document
            bulk_data.append(doc_info['enriched_doc'])
        
        # Send bulk request
        url = f"{self.es_url}/_bulk"
        headers = {"Content-Type": "application/x-ndjson"}
        # No params
        
        # Convert to newline-delimited JSON
        bulk_body = ""
        for item in bulk_data:
            bulk_body += json.dumps(item) + "\n"
        
        try:
            response = requests.post(url, headers=headers, data=bulk_body, verify=False)
            response.raise_for_status()
            
            # Check for errors in bulk response
            result = response.json()
            if result.get('errors'):
                errors = [item for item in result.get('items', []) if item.get('index', {}).get('error')]
                logger.warning(f"Some documents failed to index: {len(errors)} errors")
                for error in errors[:5]:  # Log first 5 errors
                    logger.warning(f"Error: {error.get('index', {}).get('error', {}).get('reason', 'Unknown error')}")
            
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Bulk indexing failed: {e}")
            return False
    
    def update_existing_documents(self, index_name: str, batch_size: int = 100):
        """Update existing documents in place with extracted keywords"""
        logger.info(f"🔄 Updating existing documents in: {index_name}")
        
        # Extract all documents
        documents = self.keyword_extractor.extract_documents_from_index(index_name, batch_size)
        logger.info(f"📄 Found {len(documents)} documents in {index_name}")
        
        # Process documents in batches
        success_count = 0
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            
            # Update each document in the batch
            for doc in batch:
                try:
                    enriched_doc = self.enrich_document(doc)
                    
                    # Prepare update data (only new fields)
                    update_data = {
                        'programming_language': enriched_doc.get('programming_language', []),
                        'framework': enriched_doc.get('framework', []),
                        'tool': enriched_doc.get('tool', []),
                        'concept': enriched_doc.get('concept', []),
                        'technical_terms': enriched_doc.get('technical_terms', []),
                        'content_type': enriched_doc.get('content_type', 'other'),
                        'domain': enriched_doc.get('domain', 'unknown'),
                        'entities': enriched_doc.get('entities', {}),
                        'content_length': enriched_doc.get('content_length', 'medium'),
                        'language': enriched_doc.get('language', 'en')
                    }
                    
                    # Update document
                    success = self._update_document(index_name, doc['id'], update_data)
                    if success:
                        success_count += 1
                    
                except Exception as e:
                    logger.warning(f"Error updating document {doc.get('id', 'unknown')}: {e}")
            
            logger.info(f"✅ Updated {success_count} documents so far")
        
        logger.info(f"🎉 Successfully updated {success_count}/{len(documents)} documents in {index_name}")
        return success_count == len(documents)
    
    def _update_document(self, index_name: str, doc_id: str, update_data: Dict) -> bool:
        """Update a single document with new fields"""
        url = f"{self.es_url}/{index_name}/_update/{doc_id}"
        headers = {"Content-Type": "application/json"}
        # No params
        
        update_body = {
            "doc": update_data
        }
        
        try:
            response = requests.post(url, headers=headers, json=update_body, verify=False)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update document {doc_id}: {e}")
            return False
    
    def process_all_indexes(self):
        """Process all indexes"""
        # Get indexes from config
        indexes_config = self.config.get('elasticsearch', {}).get('indexes', {})
        
        if not indexes_config:
            logger.error("❌ No indexes found in configuration")
            return
        
        logger.info("🚀 Starting document enrichment process...")
        logger.info(f"Mode: {'Create new enriched indexes' if self.create_new_index else 'Update existing documents'}")
        
        success_count = 0
        for source_index, enriched_index in indexes_config.items():
            try:
                if self.create_new_index:
                    success = self.process_index(source_index, enriched_index)
                else:
                    success = self.update_existing_documents(source_index)
                
                if success:
                    success_count += 1
                    logger.info(f"✅ Successfully processed {source_index}")
                else:
                    logger.error(f"❌ Failed to process {source_index}")
                    
            except Exception as e:
                logger.error(f"❌ Error processing {source_index}: {e}")
        
        logger.info(f"🎉 Document enrichment complete! {success_count}/{len(indexes_config)} indexes processed successfully")
        
        if self.create_new_index:
            logger.info("\n📋 New enriched indexes created:")
            for source_index, enriched_index in indexes_config.items():
                logger.info(f"  - {source_index} → {enriched_index}")
            logger.info("\n💡 Update your config.yaml to use the new enriched indexes!")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Enrich Elasticsearch documents with extracted keywords')
    parser.add_argument('--create-new', action='store_true', 
                       help='Create new enriched indexes instead of updating existing documents')
    parser.add_argument('--config', default='config.yaml',
                       help='Path to configuration file')
    
    args = parser.parse_args()
    
    try:
        # Initialize enricher
        enricher = DocumentEnricher(
            config_path=args.config,
            create_new_index=args.create_new
        )
        
        # Process all indexes
        enricher.process_all_indexes()
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        raise

if __name__ == "__main__":
    main() 