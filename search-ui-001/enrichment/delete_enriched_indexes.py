#!/usr/bin/env python3
"""
Script to delete enriched indexes for testing purposes
"""

import requests
import yaml
import sys

def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration from YAML file"""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def delete_enriched_indexes():
    """Delete all enriched indexes"""
    config = load_config()
    es_url = config['elasticsearch']['host']
    headers = {'Content-Type': 'application/json'}
    
    # Get enriched indexes from config
    indexes_config = config['elasticsearch']['indexes']
    enriched_indexes = list(indexes_config.values())
    
    print("🗑️  Deleting Enriched Indexes")
    print("=" * 50)
    
    for index in enriched_indexes:
        try:
            url = f"{es_url}/{index}"
            response = requests.delete(url, headers=headers, verify=False)
            
            if response.status_code == 200:
                print(f"✅ Deleted: {index}")
            elif response.status_code == 404:
                print(f"⚠️  Not found: {index}")
            else:
                print(f"❌ Failed to delete {index}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error deleting {index}: {e}")
    
    print("\n🎯 Enriched indexes deletion complete!")

if __name__ == "__main__":
    delete_enriched_indexes() 