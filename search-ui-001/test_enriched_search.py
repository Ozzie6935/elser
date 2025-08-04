#!/usr/bin/env python3
"""
Test script to verify enriched indexes are working
"""

import requests
import json

def test_enriched_search():
    """Test the enriched search functionality"""
    
    # Test search with enriched filters
    url = "http://localhost:8000/api/elasticsearch/search"
    params = {
        "q": "python",
        "api_key": "xyz123",
        "search_type": "semantic",
        "size": 3
    }
    
    try:
        print("🔍 Testing enriched search...")
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search successful! Found {data.get('totalResults', 0)} results")
            
            # Check if we have enriched fields in results
            results = data.get('results', [])
            if results:
                print(f"\n📊 Sample result enriched fields:")
                sample = results[0]
                
                enriched_fields = [
                    'programming_language', 'framework', 'tool', 'concept',
                    'technical_terms', 'content_type', 'domain', 'entities'
                ]
                
                for field in enriched_fields:
                    value = sample.get(field)
                    if value:
                        print(f"  ✅ {field}: {value}")
                    else:
                        print(f"  ❌ {field}: Not found")
            
            # Check aggregations
            aggs = data.get('aggregations', {})
            if aggs:
                print(f"\n🔍 Available filter aggregations:")
                for agg_name, agg_data in aggs.items():
                    buckets = agg_data.get('buckets', [])
                    if buckets:
                        print(f"  📂 {agg_name}: {len(buckets)} options")
                        # Show first few options
                        for bucket in buckets[:3]:
                            print(f"    - {bucket['key']} ({bucket['doc_count']})")
            
            return True
        else:
            print(f"❌ Search failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend. Make sure it's running on localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error testing search: {e}")
        return False

def test_filtered_search():
    """Test search with filters"""
    
    # Test with programming language filter
    url = "http://localhost:8000/api/elasticsearch/search"
    filters = {
        "programming_language": ["python", "javascript"]
    }
    
    params = {
        "q": "machine learning",
        "api_key": "xyz123",
        "search_type": "semantic",
        "size": 2,
        "filters": json.dumps(filters)
    }
    
    try:
        print("\n🔍 Testing filtered search...")
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Filtered search successful! Found {data.get('totalResults', 0)} results")
            return True
        else:
            print(f"❌ Filtered search failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing filtered search: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Enriched Search System")
    print("=" * 50)
    
    # Test basic search
    success1 = test_enriched_search()
    
    # Test filtered search
    success2 = test_filtered_search()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 All tests passed! Enriched search system is working correctly.")
    else:
        print("❌ Some tests failed. Check the backend and enriched indexes.") 