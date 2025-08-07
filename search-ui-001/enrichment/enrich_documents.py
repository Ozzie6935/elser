#!/usr/bin/env python3
"""
Simple script to enrich documents with extracted keywords
Choose between updating existing documents or creating new enriched indexes
"""

import sys
import os
from document_enricher import DocumentEnricher

def main():
    print("🚀 Document Enrichment System")
    print("="*50)
    print()
    print("This system will extract keywords from your documents and add them as new fields.")
    print("You have two options:")
    print()
    print("1. 📝 UPDATE EXISTING DOCUMENTS")
    print("   - Adds keyword fields to your existing documents")
    print("   - Keeps your current indexes")
    print("   - Faster processing")
    print("   - No need to change your application configuration")
    print()
    print("2. 🆕 CREATE NEW ENRICHED INDEXES")
    print("   - Creates new indexes with '_enriched' suffix")
    print("   - Keeps your original indexes unchanged")
    print("   - Safer approach (original data preserved)")
    print("   - Requires updating your application to use new indexes")
    print()
    
    while True:
        choice = input("Choose an option (1 or 2): ").strip()
        
        if choice == "1":
            print("\n✅ You chose to UPDATE EXISTING DOCUMENTS")
            print("⚠️  This will modify your current documents by adding new fields.")
            confirm = input("Are you sure? (yes/no): ").strip().lower()
            
            if confirm in ['yes', 'y']:
                print("\n🔄 Starting document update process...")
                enricher = DocumentEnricher(create_new_index=False)
                enricher.process_all_indexes()
                print("\n✅ Document update complete!")
                print("Your existing documents now have new keyword fields for enhanced filtering.")
                break
            else:
                print("Operation cancelled.")
                break
                
        elif choice == "2":
            print("\n✅ You chose to CREATE NEW ENRICHED INDEXES")
            print("This will create new indexes with '_enriched' suffix.")
            confirm = input("Continue? (yes/no): ").strip().lower()
            
            if confirm in ['yes', 'y']:
                print("\n🔄 Starting enriched index creation...")
                enricher = DocumentEnricher(create_new_index=True)
                enricher.process_all_indexes()
                print("\n✅ Enriched index creation complete!")
                print("\n📋 New indexes created:")
                print("  - semantic-python-index_enriched")
                print("  - semantic-elastic-co-index_enriched")
                print("  - semantic-wikipedia-index_enriched")
                print("\n💡 To use the new indexes, update your config.yaml:")
                print("   indexes:")
                print("     - semantic-python-index_enriched")
                print("     - semantic-elastic-co-index_enriched")
                print("     - semantic-wikipedia-index_enriched")
                break
            else:
                print("Operation cancelled.")
                break
                
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main() 