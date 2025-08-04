#!/usr/bin/env python3
"""
Command Line Interface for Document Enrichment Framework
"""

import argparse
import sys
import os
from typing import Optional
from core import create_enrichment_core

def setup_parser() -> argparse.ArgumentParser:
    """Setup command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Document Enrichment Framework - Add keywords, entities, and metadata to Elasticsearch documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create new enriched indexes
  python3 run_enrichment.py enrich --create-new

  # Update existing documents
  python3 run_enrichment.py enrich --update-existing

  # Process specific indexes
  python3 run_enrichment.py enrich --create-new --indexes semantic-python-index

  # Extract keywords only (no enrichment)
  python3 run_enrichment.py extract --index semantic-python-index

  # Verify enriched indexes
  python3 run_enrichment.py verify

  # Check source indexes
  python3 run_enrichment.py check-sources

  # Delete enriched indexes
  python3 run_enrichment.py delete-enriched

  # Show this help
  python3 run_enrichment.py --help
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Enrich command
    enrich_parser = subparsers.add_parser('enrich', help='Enrich documents with keywords, entities, and metadata')
    enrich_parser.add_argument('--create-new', action='store_true', 
                              help='Create new enriched indexes')
    enrich_parser.add_argument('--update-existing', action='store_true',
                              help='Update existing documents in place')
    enrich_parser.add_argument('--indexes', nargs='+', 
                              help='Specific indexes to process (default: all from config)')
    enrich_parser.add_argument('--config', default='config.yaml',
                              help='Path to configuration file')
    enrich_parser.add_argument('--batch-size', type=int, default=100,
                              help='Batch size for processing (default: 100)')
    enrich_parser.add_argument('--dry-run', action='store_true',
                              help='Show what would be done without making changes')
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract keywords from documents (without enrichment)')
    extract_parser.add_argument('--index', required=True,
                               help='Index to extract keywords from')
    extract_parser.add_argument('--output', default='keywords_output.json',
                               help='Output file for keywords (default: keywords_output.json)')
    extract_parser.add_argument('--config', default='config.yaml',
                               help='Path to configuration file')
    
    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify enriched indexes and show statistics')
    verify_parser.add_argument('--config', default='config.yaml',
                              help='Path to configuration file')
    verify_parser.add_argument('--detailed', action='store_true',
                              help='Show detailed verification information')
    
    # Check sources command
    check_parser = subparsers.add_parser('check-sources', help='Check source indexes and document counts')
    check_parser.add_argument('--config', default='config.yaml',
                             help='Path to configuration file')
    
    # Delete enriched command
    delete_parser = subparsers.add_parser('delete-enriched', help='Delete enriched indexes (use with caution)')
    delete_parser.add_argument('--config', default='config.yaml',
                              help='Path to configuration file')
    delete_parser.add_argument('--confirm', action='store_true',
                              help='Skip confirmation prompt')
    
    return parser

def enrich_command(args: argparse.Namespace) -> int:
    """Handle enrich command"""
    print("🚀 Document Enrichment Framework")
    print("=" * 50)
    print()
    
    # Validate arguments
    if not args.create_new and not args.update_existing:
        print("❌ Error: Must specify either --create-new or --update-existing")
        return 1
    
    if args.create_new and args.update_existing:
        print("❌ Error: Cannot use both --create-new and --update-existing")
        return 1
    
    try:
        # Initialize core with correct mode
        core = create_enrichment_core(args.config, create_new_index=args.create_new)
        
        if args.dry_run:
            print("🔍 DRY RUN MODE - No changes will be made")
            print()
            
            # Show what would be processed
            index_info = core.get_index_info()
            if args.indexes:
                print(f"📋 Would process indexes: {args.indexes}")
            else:
                print(f"📋 Would process all indexes: {index_info['source_indexes']}")
            
            print(f"🔧 Mode: {'Create new enriched indexes' if args.create_new else 'Update existing documents'}")
            print(f"📦 Batch size: {args.batch_size}")
            return 0
        
        # Process indexes
        if args.create_new:
            results = core.create_enriched_indexes(args.indexes, args.batch_size, args.dry_run)
        else:
            results = core.update_existing_documents(args.indexes, args.batch_size, args.dry_run)
        
        # Show results
        success_count = sum(1 for success in results.values() if success)
        total_count = len(results)
        
        print(f"\n🎉 Processing complete! {success_count}/{total_count} indexes processed successfully")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error during enrichment: {e}")
        return 1

def extract_command(args: argparse.Namespace) -> int:
    """Handle extract command"""
    print("🔍 Keyword Extraction")
    print("=" * 30)
    print()
    
    try:
        # Initialize core
        core = create_enrichment_core(args.config)
        
        print(f"📋 Extracting keywords from: {args.index}")
        print(f"💾 Output file: {args.output}")
        print()
        
        # Extract keywords
        keywords = core.extract_keywords(args.index, args.output)
        
        print(f"✅ Keywords extracted and saved to {args.output}")
        print(f"📊 Total keywords: {len(keywords['technical_terms'])}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error during extraction: {e}")
        return 1

def verify_command(args: argparse.Namespace) -> int:
    """Handle verify command"""
    print("🔍 Verification")
    print("=" * 20)
    print()
    
    try:
        # Import verification functions
        from verification import verify_enriched_fields, check_index_stats
        
        # Run verification
        verify_enriched_fields()
        check_index_stats()
        
        if args.detailed:
            print("\n🔍 Running detailed verification...")
            from verification import detailed_verification
            detailed_verification.examine_document_content()
        
        return 0
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return 1

def check_sources_command(args: argparse.Namespace) -> int:
    """Handle check-sources command"""
    print("🔍 Checking Source Indexes")
    print("=" * 30)
    print()
    
    try:
        from check_source_indexes import check_source_indexes
        check_source_indexes()
        return 0
        
    except Exception as e:
        print(f"❌ Error checking sources: {e}")
        return 1

def delete_enriched_command(args: argparse.Namespace) -> int:
    """Handle delete-enriched command"""
    print("🗑️  Delete Enriched Indexes")
    print("=" * 30)
    print()
    
    try:
        from delete_enriched_indexes import delete_enriched_indexes
        
        if not args.confirm:
            response = input("⚠️  Are you sure you want to delete all enriched indexes? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Operation cancelled")
                return 0
        
        delete_enriched_indexes()
        return 0
        
    except Exception as e:
        print(f"❌ Error deleting enriched indexes: {e}")
        return 1

def main():
    """Main CLI entry point"""
    parser = setup_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Route to appropriate command handler
    command_handlers = {
        'enrich': enrich_command,
        'extract': extract_command,
        'verify': verify_command,
        'check-sources': check_sources_command,
        'delete-enriched': delete_enriched_command
    }
    
    handler = command_handlers.get(args.command)
    if handler:
        return handler(args)
    else:
        print(f"❌ Unknown command: {args.command}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 