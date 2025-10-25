import os
import re
import time
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ManimCodeGenerator:
    """
    A class that uses LangChain with Google's Gemini API to generate 
    Manim code for educational videos in the style of 3Blue1Brown.
    """
    
    def __init__(self):
        """Initialize the Manim code generator with Gemini AI."""
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        # Initialize the Gemini model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=self.api_key,
            temperature=0.7,
            max_tokens=4096
        )
        
        # Create the prompt template for 3Blue1Brown style Manim code
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            ("human", "{educational_content}")
        ])
    
    def _get_system_prompt(self) -> str:
        """Return the system prompt for generating 3Blue1Brown style Manim code."""
        return """
You are an expert at creating educational video animations using Manim (Mathematical Animation Engine) 
in the distinctive style of 3Blue1Brown (Grant Sanderson). Your task is to generate clean, well-commented 
Python code using the Manim library that creates engaging mathematical and educational visualizations.

Key characteristics of 3Blue1Brown style:
1. Clean, minimalist aesthetic with a dark background
2. Smooth, purposeful animations that build understanding step by step
3. Mathematical rigor combined with intuitive explanations
4. Strategic use of color to highlight important concepts
5. Clear typography and well-positioned text
6. Gradual revelation of information to maintain engagement
7. Use of geometric shapes, graphs, and mathematical objects
8. Emphasis on visual metaphors and analogies

Guidelines for your Manim code:
- Always inherit from Scene class
- Use appropriate Manim objects (Text, MathTex, VGroup, etc.)
- Include smooth animations with proper timing
- Use the 3Blue1Brown color palette (BLUE, YELLOW, GREEN, RED, etc.)
- Add clear comments explaining each step
- Structure the code with logical sections
- Use self.play() for animations and self.wait() for pauses
- Include both creation and transformation animations
- Make sure the code is executable and follows Manim syntax

The code should be production-ready and create a complete educational video segment.
Generate ONLY the Python code for the Manim scene, with no additional explanation unless specifically requested.
"""

    def generate_manim_code(self, educational_content: str, save_to_file: bool = True) -> str:
        """
        Generate Manim code based on the given educational content.
        
        Args:
            educational_content (str): The educational topic or content to visualize
            save_to_file (bool): Whether to save the generated code to topic_manim.py (default: True)
            
        Returns:
            str: Complete Manim Python code for creating the educational video
        """
        try:
            # Create the prompt
            prompt = self.prompt_template.format_messages(
                educational_content=educational_content
            )
            
            # Generate the response
            response = self.llm.invoke(prompt)
            
            # Extract and clean the code
            manim_code = response.content.strip()
            
            # Ensure the code starts with proper imports if not included
            if "from manim import *" not in manim_code:
                imports = "from manim import *\nimport numpy as np\n\n"
                manim_code = imports + manim_code
            
            # Save to file if requested
            if save_to_file:
                # Create filename from topic
                clean_topic = re.sub(r'[^a-zA-Z0-9\s]', '', educational_content)
                clean_topic = re.sub(r'\s+', '_', clean_topic.strip())
                clean_topic = clean_topic.lower()[:50]  # Limit length
                output_filename = f"{clean_topic}_manim.py"
                
                with open(output_filename, 'w', encoding='utf-8') as f:
                    f.write(manim_code)
                print(f"✅ Generated Manim code saved to: {output_filename}")
            
            return manim_code
            
        except Exception as e:
            raise Exception(f"Error generating Manim code: {str(e)}")
    
    def generate_advanced_manim_code(self, 
                                   educational_content: str, 
                                   video_length: Optional[int] = None,
                                   difficulty_level: str = "intermediate") -> str:
        """
        Generate advanced Manim code with additional parameters.
        
        Args:
            educational_content (str): The educational topic or content to visualize
            video_length (Optional[int]): Desired video length in seconds
            difficulty_level (str): Target difficulty level ("beginner", "intermediate", "advanced")
            
        Returns:
            str: Complete Manim Python code for creating the educational video
        """
        enhanced_prompt = f"""
        Educational Content: {educational_content}
        
        Additional Requirements:
        - Target difficulty level: {difficulty_level}
        {f"- Target video length: approximately {video_length} seconds" if video_length else ""}
        - Include multiple scenes if the content is complex
        - Add voice-over timing comments for narration
        - Use advanced Manim features where appropriate
        
        Create a comprehensive educational video that progressively builds understanding 
        of the topic while maintaining the 3Blue1Brown aesthetic and teaching style.
        """
        
        return self.generate_manim_code(enhanced_prompt)

    def validate_manim_code(self, code: str) -> tuple[bool, str]:
        """
        Basic validation of the generated Manim code.
        
        Args:
            code (str): The Manim code to validate
            
        Returns:
            tuple[bool, str]: (is_valid, error_message)
        """
        try:
            # Basic syntax validation
            compile(code, '<string>', 'exec')
            
            # Check for required Manim components
            required_elements = [
                "class",
                "Scene",
                "def construct",
                "self.play"
            ]
            
            for element in required_elements:
                if element not in code:
                    return False, f"Missing required element: {element}"
            
            return True, "Code appears valid"
            
        except SyntaxError as e:
            return False, f"Syntax error: {str(e)}"
        except Exception as e:
            return False, f"Validation error: {str(e)}"

def generate_video(prompt: str) -> str:
    """
    Generate a Manim video file from a text prompt.
    
    This function takes an educational prompt, generates 3Blue1Brown-style Manim code,
    validates it, and saves it to a Python file that can be executed with Manim.
    
    Args:
        prompt (str): The educational content or topic to create a video about
        
    Returns:
        str: Path to the generated Python file containing Manim code
        
    Raises:
        Exception: If code generation or file creation fails
    """
    
    try:
        # Initialize the generator
        generator = ManimCodeGenerator()
        
        # Generate the Manim code
        manim_code = generator.generate_manim_code(prompt)
        
        # Validate the generated code
        is_valid, validation_message = generator.validate_manim_code(manim_code)
        if not is_valid:
            raise Exception(f"Generated code validation failed: {validation_message}")
        
        # Create a filename based on the prompt
        # Clean the prompt to create a valid filename
        clean_prompt = re.sub(r'[^a-zA-Z0-9\s]', '', prompt)
        clean_prompt = re.sub(r'\s+', '_', clean_prompt.strip())
        clean_prompt = clean_prompt.lower()[:50]  # Limit length
        
        # Add timestamp to ensure uniqueness
        timestamp = int(time.time())
        filename = f"{clean_prompt}_{timestamp}_manim.py"
        
        # Create the output directory if it doesn't exist
        output_dir = "generated_videos"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Full path to the file
        file_path = os.path.join(output_dir, filename)
        
        # Save the code to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(manim_code)
        
        return file_path
        
    except Exception as e:
        raise Exception(f"Error in generate_video: {str(e)}")

# Example usage and utility functions
def create_educational_video(topic: str, 
                           difficulty: str = "intermediate", 
                           duration: Optional[int] = None) -> str:
    """
    Convenience function to generate Manim code for educational videos.
    
    Args:
        topic (str): The educational topic to create a video about
        difficulty (str): Difficulty level ("beginner", "intermediate", "advanced")
        duration (Optional[int]): Target duration in seconds
        
    Returns:
        str: Generated Manim code
    """
    generator = ManimCodeGenerator()
    return generator.generate_advanced_manim_code(
        educational_content=topic,
        difficulty_level=difficulty,
        video_length=duration
    )

def validate_and_save_code(code: str, filename: str = "educational_scene.py") -> bool:
    """
    Validate and save the generated Manim code to a file.
    
    Args:
        code (str): The Manim code to save
        filename (str): The filename to save to
        
    Returns:
        bool: True if successful, False otherwise
    """
    generator = ManimCodeGenerator()
    is_valid, message = generator.validate_manim_code(code)
    
    if is_valid:
        try:
            with open(filename, 'w') as f:
                f.write(code)
            print(f"Code saved successfully to {filename}")
            return True
        except Exception as e:
            print(f"Error saving file: {str(e)}")
            return False
    else:
        print(f"Code validation failed: {message}")
        return False

# Example topics for testing
EXAMPLE_TOPICS = [
    "Explain the concept of derivatives using geometric intuition",
    "Visualize how neural networks learn through backpropagation",
    "Demonstrate the beauty of Euler's identity e^(iπ) + 1 = 0",
    "Show how Fourier transforms decompose signals into frequencies",
    "Illustrate the concept of limits in calculus",
    "Explain linear algebra transformations and their geometric meaning",
    "Visualize the proof of the Pythagorean theorem",
    "Demonstrate how probability distributions work"
]

if __name__ == "__main__":
    # Example usage
    generator = ManimCodeGenerator()
    
    # Generate code for a mathematical concept
    topic = "Explain the concept of derivatives using geometric intuition"
    code = generator.generate_manim_code(topic)
    
    print("Generated Manim Code:")
    print("=" * 50)
    print(code)
    print("=" * 50)
    
    # Validate the code
    is_valid, message = generator.validate_manim_code(code)
    print(f"Code validation: {message}")