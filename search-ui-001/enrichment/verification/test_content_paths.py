#!/usr/bin/env python3
"""
Test script to verify configurable content paths work correctly
"""

import yaml
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from keyword_extractor import SmartKeywordExtractor

def test_content_paths():
    """Test the configurable content paths functionality"""
    print("🧪 Testing Configurable Content Paths")
    print("=" * 50)
    print()
    
    # Load config
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    content_paths = config.get('content_paths', {})
    print("📋 Current content paths configuration:")
    for key, path in content_paths.items():
        print(f"  {key}: {path}")
    print()
    
    # Test the _get_content_by_path method
    extractor = SmartKeywordExtractor()
    
    # Test document with current structure
    test_doc = {
        'content': {
            'body': {
                'clean_content': 'This is clean content',
                'raw_html': '<html>This is raw HTML</html>'
            }
        },
        'title': {
            'raw': 'Test Title'
        },
        'description': {
            'raw': 'Test Description'
        },
        'url': {
            'raw': 'https://example.com'
        }
    }
    
    print("🔍 Testing content extraction with current paths:")
    for key, path in content_paths.items():
        content = extractor._get_content_by_path(test_doc, path)
        print(f"  {key} ({path}): '{content}'")
    print()
    
    # Test with different document structure
    alt_doc = {
        'text': {
            'clean': 'Alternative clean content',
            'html': '<html>Alternative HTML</html>'
        },
        'page': {
            'title': 'Alternative Title',
            'description': 'Alternative Description'
        },
        'link': 'https://alternative.com'
    }
    
    print("🔍 Testing with alternative document structure:")
    alt_paths = {
        'clean_content': 'text.clean',
        'raw_html': 'text.html',
        'title': 'page.title',
        'description': 'page.description',
        'url': 'link'
    }
    
    for key, path in alt_paths.items():
        content = extractor._get_content_by_path(alt_doc, path)
        print(f"  {key} ({path}): '{content}'")
    print()
    
    print("✅ Content path testing completed!")

if __name__ == "__main__":
    test_content_paths() 