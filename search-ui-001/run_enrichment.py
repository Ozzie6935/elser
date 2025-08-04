#!/usr/bin/env python3
"""
Runner script for the enrichment framework
This script can be run from the root directory
"""

import sys
import os
import subprocess
import argparse

def main():
    """Main function to run enrichment"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Document Enrichment Framework Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default settings (create new enriched indexes)
  python3 run_enrichment.py

  # Show help for CLI options
  python3 run_enrichment.py --help

  # Pass arguments to the CLI
  python3 run_enrichment.py enrich --create-new
  python3 run_enrichment.py enrich --update-existing
  python3 run_enrichment.py verify
  python3 run_enrichment.py check-sources
        """
    )
    parser.add_argument('cli_args', nargs=argparse.REMAINDER,
                       help='Arguments to pass to the CLI')
    
    args = parser.parse_args()
    
    print("🔧 Document Enrichment Framework Runner")
    print("=" * 50)
    print()
    
    # Get the directory where this script is located
    root_dir = os.path.dirname(os.path.abspath(__file__))
    enrichment_dir = os.path.join(root_dir, 'enrichment')
    venv_dir = os.path.join(root_dir, 'venv')
    
    # Check if virtual environment exists
    if not os.path.exists(venv_dir):
        print("❌ Virtual environment not found!")
        print(f"Expected location: {venv_dir}")
        print("Please create a virtual environment first:")
        print("python -m venv venv")
        sys.exit(1)
    
    # Change to enrichment directory
    os.chdir(enrichment_dir)
    
    # Activate virtual environment and run enrichment
    try:
        # Use the virtual environment's Python interpreter
        venv_python = os.path.join(venv_dir, 'bin', 'python')
        if not os.path.exists(venv_python):
            venv_python = os.path.join(venv_dir, 'Scripts', 'python.exe')  # Windows
        
        print(f"📍 Running from: {enrichment_dir}")
        print(f"🐍 Using Python: {venv_python}")
        print()
        
        # Build command for CLI
        cmd = [venv_python, "cli.py"]
        
        if args.cli_args:
            # Use provided CLI arguments
            cmd.extend(args.cli_args)
        else:
            # Show help when no arguments provided
            print("🚀 Document Enrichment Framework")
            print("=" * 50)
            print("No arguments provided. Showing help:")
            print()
            cmd.extend(["--help"])
        
        # Run the CLI
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n🛑 Enrichment stopped by user")
    except Exception as e:
        print(f"❌ Error running enrichment: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 