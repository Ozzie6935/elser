#!/usr/bin/env python3
"""
Update Elasticsearch mapping with new keyword fields for enhanced aggregations
"""

import json
import requests
import yaml
from typing import Dict, List

def load_config(config_path: str = "config.yaml") -> Dict:
    """Load configuration from YAML file"""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def update_index_mapping(index_name: str, mapping: Dict, config: Dict):
    """Update the mapping for a specific index"""
    es_url = config['elasticsearch']['url']
    api_key = config['api']['key']
    
    url = f"{es_url}/{index_name}/_mapping"
    headers = {"Content-Type": "application/json"}
    params = {"api_key": api_key}
    
    try:
        response = requests.put(url, headers=headers, params=params, json=mapping, verify=False)
        response.raise_for_status()
        print(f"✅ Successfully updated mapping for {index_name}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to update mapping for {index_name}: {e}")
        return False

def create_enhanced_mapping() -> Dict:
    """Create enhanced mapping with keyword fields for aggregations"""
    mapping = {
        "properties": {
            # Existing fields (keep as is)
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
                    "gpe": {  # Geo-Political Entity
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
    
    return mapping

def main():
    """Main function to update all index mappings"""
    try:
        # Load configuration
        config = load_config()
        
        # Create enhanced mapping
        mapping = create_enhanced_mapping()
        
        # Indexes to update
        indexes = [
            'semantic-python-index',
            'semantic-elastic-co-index', 
            'semantic-wikipedia-index'
        ]
        
        print("🔄 Updating Elasticsearch mappings with new keyword fields...")
        print("="*60)
        
        success_count = 0
        for index_name in indexes:
            if update_index_mapping(index_name, mapping, config):
                success_count += 1
        
        print(f"\n📊 Summary: {success_count}/{len(indexes)} indexes updated successfully")
        
        if success_count == len(indexes):
            print("\n✅ All mappings updated successfully!")
            print("\nNew aggregation fields available:")
            print("  - programming_language")
            print("  - framework") 
            print("  - tool")
            print("  - concept")
            print("  - content_type")
            print("  - domain")
            print("  - technical_terms")
            print("  - entities.*")
            print("  - content_length")
            print("  - language")
        else:
            print("\n⚠️  Some mappings failed to update. Check the errors above.")
    
    except Exception as e:
        print(f"❌ Error updating mappings: {e}")

if __name__ == "__main__":
    main() 