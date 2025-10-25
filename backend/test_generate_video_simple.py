#!/usr/bin/env python3
"""
Simple test script to test only the generate_video function.
This script generates Manim code from a text prompt.
"""

import os
import sys
from ai import generate_video

def main():
    print("🎬 Testing generate_video Function")
    print("=" * 60)
    
    # Check if Google API key is set
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_google_api_key_here":
        print("\n❌ ERROR: Google API key not found!")
        print("\nTo use this function, you need to:")
        print("1. Get a Google API key from: https://makersuite.google.com/app/apikey")
        print("2. Create a .env file in the backend directory")
        print("3. Add this line to .env:")
        print("   GOOGLE_API_KEY=your_actual_api_key_here")
        print("\n💡 Tip: Copy .env.example to .env and update it with your key")
        return
    
    # Test prompt
    prompt = input("\n📝 Enter your topic (or press Enter for default): ").strip()
    
    if not prompt:
        prompt = "Explain the Pythagorean theorem with visual proof"
        print(f"Using default prompt: '{prompt}'")
    
    print(f"\n🚀 Generating Manim code for: '{prompt}'")
    print("-" * 60)
    
    try:
        # Call generate_video function
        file_path = generate_video(prompt)
        
        print("\n✅ SUCCESS!")
        print(f"📁 File generated at: {file_path}")
        print("\n🎨 To render the animation, run:")
        print(f"   manim {file_path} -pql")
        
        # Show file size
        file_size = os.path.getsize(file_path)
        print(f"\n📊 File size: {file_size} bytes")
        print(f"📁 File path: {file_path}")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
