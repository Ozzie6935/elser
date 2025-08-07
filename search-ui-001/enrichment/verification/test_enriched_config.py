#!/usr/bin/env python3
"""
Test the updated config.yaml with enriched indexes
"""

import requests
import json
import yaml
from typing import Dict, List

def load_config(config_path: str = "config.yaml") -> Dict:
    """Load configuration from YAML file"""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def test_enriched_indexes():
    """Test that the enriched indexes are accessible and working"""
    config = load_config()
    es_url = config['elasticsearch']['host']
    headers = {'Content-Type': 'application/json'}
    
    print("🔍 Testing Updated Config with Enriched Indexes")
    print("=" * 60)
    print()
    
    # Get the indexes from config
    indexes_config = config['elasticsearch']['indexes']
    print(f"📋 Configured indexes: {indexes_config}")
    print()
    
    total_docs = 0
    total_keywords = 0
    
    # For verification, we want to test the enriched indexes
    enriched_indexes = list(indexes_config.values())
    
    for index in enriched_indexes:
        print(f"🔍 Testing index: {index}")
        print("-" * 40)
        
        try:
            # Test basic connectivity
            count_url = f'{es_url}/{index}/_count'
            count_response = requests.post(count_url, headers=headers, json={'query': {'match_all': {}}}, verify=False)
            count_response.raise_for_status()
            
            doc_count = count_response.json().get('count', 0)
            total_docs += doc_count
            print(f"✅ Connected successfully - {doc_count} documents")
            
            # Test enriched fields
            if doc_count > 0:
                search_url = f'{es_url}/{index}/_search'
                search_query = {
                    'size': 1,
                    'query': {'match_all': {}},
                    '_source': ['programming_language', 'framework', 'tool', 'concept', 'technical_terms', 'entities']
                }
                
                search_response = requests.post(search_url, headers=headers, json=search_query, verify=False)
                search_response.raise_for_status()
                
                data = search_response.json()
                hits = data.get('hits', {}).get('hits', [])
                
                if hits:
                    doc = hits[0]['_source']
                    
                    # Count keywords
                    keywords_found = 0
                    for field in ['programming_language', 'framework', 'tool', 'concept', 'technical_terms']:
                        value = doc.get(field, [])
                        if isinstance(value, list):
                            keywords_found += len(value)
                    
                    total_keywords += keywords_found
                    print(f"✅ Enriched fields present - {keywords_found} keywords found")
                    
                    # Show sample data
                    if doc.get('programming_language'):
                        print(f"   Sample languages: {doc['programming_language'][:3]}")
                    if doc.get('technical_terms'):
                        print(f"   Sample terms: {doc['technical_terms'][:3]}")
                else:
                    print("⚠️  No documents found in search results")
            else:
                print("⚠️  No documents in index")
            
            print()
            
        except Exception as e:
            print(f"❌ Error testing {index}: {e}")
            print()
    
    # Summary
    print("📊 CONFIG TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Total documents accessible: {total_docs}")
    print(f"🔧 Total keywords available: {total_keywords}")
    print(f"📈 Average keywords per document: {total_keywords/total_docs:.1f}" if total_docs > 0 else "📈 Average keywords per document: 0")
    print()
    
    if total_docs > 0 and total_keywords > 0:
        print("🎉 SUCCESS! Your application is now configured to use enriched indexes.")
        print("💡 You can now:")
        print("   - Filter by programming languages, frameworks, tools, and concepts")
        print("   - Search by technical terms")
        print("   - Use entity-based filtering")
        print("   - Build faceted search interfaces")
        print("   - Create advanced aggregations")
    else:
        print("⚠️  No enriched data found. Please check the enrichment process.")

if __name__ == "__main__":
    test_enriched_indexes() 