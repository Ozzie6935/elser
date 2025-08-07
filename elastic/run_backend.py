#!/usr/bin/env python3
"""
Runner script for the FastAPI backend
This script can be run from the root directory
"""

import sys
import os
import subprocess

def main():
    """Main function to run the backend"""
    print("🚀 FastAPI Backend Runner")
    print("=" * 40)
    print()
    
    # Get the directory where this script is located
    root_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(root_dir, 'backend')
    venv_dir = os.path.join(root_dir, 'venv')
    
    # Check if virtual environment exists
    if not os.path.exists(venv_dir):
        print("❌ Virtual environment not found!")
        print(f"Expected location: {venv_dir}")
        print("Please create a virtual environment first:")
        print("python -m venv venv")
        sys.exit(1)
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Activate virtual environment and run the backend
    try:
        # Use the virtual environment's Python interpreter
        venv_python = os.path.join(venv_dir, 'bin', 'python')
        if not os.path.exists(venv_python):
            venv_python = os.path.join(venv_dir, 'Scripts', 'python.exe')  # Windows
        
        print(f"📍 Running backend from: {backend_dir}")
        print(f"🐍 Using Python: {venv_python}")
        print()
        
        # Run the FastAPI application
        subprocess.run([venv_python, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
        
    except KeyboardInterrupt:
        print("\n🛑 Backend stopped by user")
    except Exception as e:
        print(f"❌ Error running backend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 