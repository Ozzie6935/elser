#!/usr/bin/env python3
"""
Setup script for NLP dependencies
"""

import nltk
import sys

def download_nltk_data():
    """Download required NLTK data"""
    print("🔧 Setting up NLTK data...")
    
    required_packages = [
        'punkt',
        'averaged_perceptron_tagger',
        'maxent_ne_chunker',
        'words',
        'stopwords'
    ]
    
    for package in required_packages:
        try:
            print(f"📦 Downloading {package}...")
            nltk.download(package, quiet=True)
            print(f"✅ {package} downloaded successfully")
        except Exception as e:
            print(f"❌ Error downloading {package}: {e}")
    
    print("🎉 NLTK setup complete!")

if __name__ == "__main__":
    download_nltk_data() 