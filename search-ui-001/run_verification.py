#!/usr/bin/env python3
"""
Verification runner script for the enrichment framework
This script can be run from the root directory
"""

import sys
import os
import subprocess

def main():
    """Main function to run verification"""
    print("🔍 Document Enrichment Verification Runner")
    print("=" * 60)
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
    
    # Activate virtual environment and run verification
    try:
        # Use the virtual environment's Python interpreter
        venv_python = os.path.join(venv_dir, 'bin', 'python')
        if not os.path.exists(venv_python):
            venv_python = os.path.join(venv_dir, 'Scripts', 'python.exe')  # Windows
        
        print(f"📍 Running verification from: {enrichment_dir}")
        print(f"🐍 Using Python: {venv_python}")
        print()
        
        # Run verification scripts directly
        print("🔍 Running verification scripts...")
        
        verification_scripts = [
            "verification/test_enriched_config.py",
            "verification/verify_enriched_fields.py",
            "verification/detailed_verification.py",
            "verification/final_verification_summary.py",
            "verification/test_content_paths.py",
            "verification/test_backend_enriched.py"
        ]
        
        for script in verification_scripts:
            print(f"\n🔍 Running {script}...")
            subprocess.run([venv_python, script], check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Verification stopped by user")
    except Exception as e:
        print(f"❌ Error running verification: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 