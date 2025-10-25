#!/usr/bin/env python3
"""
Test script for the generate_video function.
This demonstrates how to use the AI system to generate Manim code.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path so we can import ai.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from ai import generate_video, ManimCodeGenerator, EXAMPLE_TOPICS
    
    def test_generate_video():
        """Test the generate_video function with an example topic."""
        
        # Check if Google API key is available
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key or api_key == "your_google_api_key_here":
            print("❌ Error: Google API key not found!")
            print("To use this function:")
            print("1. Get a Google API key from https://console.cloud.google.com/")
            print("2. Enable the Gemini API")
            print("3. Create a .env file in the backend directory")
            print("4. Add: GOOGLE_API_KEY=your_actual_api_key")
            return False
        
        print("🚀 Testing the generate_video function...")
        print("=" * 50)
        
        # Test with a simple topic
        test_topic = "Explain the concept of derivatives using geometric intuition"
        print(f"📝 Topic: {test_topic}")
        
        try:
            # Generate the video file
            file_path = generate_video(test_topic)
            print(f"✅ Success! Generated file: {file_path}")
            
            # Check if file exists and show some info
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"📁 File size: {file_size} bytes")
                
                # Show first few lines of the generated code
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[:20]  # First 20 lines
                    print("\n📄 Generated Manim code preview:")
                    print("-" * 40)
                    for i, line in enumerate(lines, 1):
                        print(f"{i:2d}: {line.rstrip()}")
                    if len(lines) == 20:
                        print("    ... (truncated)")
                    print("-" * 40)
                
                print(f"\n🎬 To render this video, run:")
                print(f"   manim {file_path} -pql")
                
                return True
            else:
                print("❌ Error: File was not created")
                return False
                
        except Exception as e:
            print(f"❌ Error generating video: {str(e)}")
            return False
    
    def show_example_topics():
        """Show available example topics."""
        print("\n📚 Available example topics:")
        print("=" * 50)
        for i, topic in enumerate(EXAMPLE_TOPICS, 1):
            print(f"{i:2d}. {topic}")
    
    def manual_test():
        """Allow manual testing with custom topics."""
        print("\n🔧 Manual Testing Mode")
        print("=" * 50)
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key or api_key == "your_google_api_key_here":
            print("❌ Error: Google API key not found! Cannot proceed with manual testing.")
            return
        
        while True:
            print("\nOptions:")
            print("1. Use an example topic")
            print("2. Enter a custom topic")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                show_example_topics()
                try:
                    topic_num = int(input(f"\nSelect topic number (1-{len(EXAMPLE_TOPICS)}): "))
                    if 1 <= topic_num <= len(EXAMPLE_TOPICS):
                        topic = EXAMPLE_TOPICS[topic_num - 1]
                        print(f"\n🎯 Selected: {topic}")
                        file_path = generate_video(topic)
                        print(f"✅ Generated: {file_path}")
                    else:
                        print("❌ Invalid topic number")
                except (ValueError, IndexError):
                    print("❌ Invalid input")
                except Exception as e:
                    print(f"❌ Error: {str(e)}")
                    
            elif choice == "2":
                topic = input("\nEnter your custom topic: ").strip()
                if topic:
                    try:
                        print(f"\n🎯 Generating video for: {topic}")
                        file_path = generate_video(topic)
                        print(f"✅ Generated: {file_path}")
                    except Exception as e:
                        print(f"❌ Error: {str(e)}")
                else:
                    print("❌ Topic cannot be empty")
                    
            elif choice == "3":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice")

    if __name__ == "__main__":
        print("🎨 3Blue1Brown Style Manim Code Generator")
        print("=" * 50)
        
        # Run automatic test first
        success = test_generate_video()
        
        if success:
            # If test passed, offer manual testing
            print("\n" + "=" * 50)
            manual_choice = input("Would you like to try manual testing? (y/n): ").strip().lower()
            if manual_choice in ['y', 'yes']:
                manual_test()
        else:
            print("\n" + "=" * 50)
            print("Please set up your Google API key and try again.")

except ImportError as e:
    print(f"❌ Import Error: {str(e)}")
    print("Make sure you're running this from the backend directory.")
except Exception as e:
    print(f"❌ Unexpected Error: {str(e)}")
