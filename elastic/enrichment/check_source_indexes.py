#!/usr/bin/env python3
"""
Script to check source indexes and their content
"""

import requests
import yaml
import json

def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration from YAML file"""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def check_source_indexes():
    """Check source indexes and their content"""
    config = load_config()
    es_url = config['elasticsearch']['host']
    headers = {'Content-Type': 'application/json'}
    
    # Get source indexes from config
    indexes_config = config['elasticsearch']['indexes']
    source_indexes = list(indexes_config.keys())
    
    print("🔍 Checking Source Indexes")
    print("=" * 50)
    
    for index in source_indexes:
        try:
            # Check if index exists
            url = f"{es_url}/{index}"
            response = requests.head(url, headers=headers, verify=False)
            
            if response.status_code == 200:
                print(f"✅ Index exists: {index}")
                
                # Get document count
                count_url = f"{es_url}/{index}/_count"
                count_response = requests.get(count_url, headers=headers, verify=False)
                
                if count_response.status_code == 200:
                    count_data = count_response.json()
                    doc_count = count_data.get('count', 0)
                    print(f"   📄 Documents: {doc_count}")
                    
                    # Get one sample document
                    if doc_count > 0:
                        sample_url = f"{es_url}/{index}/_search"
                        sample_query = {"size": 1, "query": {"match_all": {}}}
                        sample_response = requests.post(sample_url, headers=headers, json=sample_query, verify=False)
                        
                        if sample_response.status_code == 200:
                            sample_data = sample_response.json()
                            hits = sample_data.get('hits', {}).get('hits', [])
                            
                            if hits:
                                doc = hits[0]['_source']
                                doc_id = hits[0]['_id']
                                
                                # Check content fields
                                content_body = doc.get('content', {}).get('body', {})
                                clean_content = content_body.get('clean_content', '')
                                raw_html = content_body.get('raw_html', '')
                                
                                print(f"   📝 Sample document ID: {doc_id}")
                                print(f"   📏 Clean content length: {len(clean_content)} characters")
                                print(f"   📏 Raw HTML length: {len(raw_html)} characters")
                                
                                # Show available fields
                                fields = list(doc.keys())
                                print(f"   📋 Available fields: {len(fields)}")
                                print(f"      {', '.join(fields[:10])}{'...' if len(fields) > 10 else ''}")
                
            elif response.status_code == 404:
                print(f"❌ Index not found: {index}")
            else:
                print(f"⚠️  Error checking {index}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error checking {index}: {e}")
        
        print()
    
    print("🎯 Source indexes check complete!")

if __name__ == "__main__":
    check_source_indexes() 