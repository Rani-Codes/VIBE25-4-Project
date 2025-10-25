import os
import re
import time
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
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
in the distinctive visual and narrative style of 3Blue1Brown (Grant Sanderson). Your task is to generate
complete, clean, and fully functional Manim Python code that creates smooth, intuitive, and visually
engaging mathematical or educational visualizations.

Core Directives:
- Output ONLY the Python code (no markdown, no explanations, no commentary outside code)
- Code must run successfully in Manim without edits
- Begin directly with 'from manim import *' or the class definition
- Always define exactly ONE scene class that inherits from Scene
- The output must form a self-contained, complete video segment

Style & Visual Identity (3Blue1Brown-inspired):
1. Dark minimalist background (default Manim dark theme)
2. Smooth and purposeful animations
3. Color cues for intuition (use BLUE, YELLOW, GREEN, RED, ORANGE, PURPLE)
4. Clear and legible text using Text and MathTex
5. Step-by-step revelation of concepts to build understanding
6. Strategic composition: centered layout, balanced spacing, use of VGroup where appropriate
7. Combination of geometry, graphs, and equations for conceptual clarity
8. Elegantly timed transitions using self.wait(), FadeIn, Write, Transform, etc.
9. Only use the basic colors and shapes available in base Manim without any external libraries or custom color definitions.

Technical Guidelines:
- Inherit from Scene (e.g., class MyScene(Scene):)
- Use MathTex for equations and Text for regular words
- Use self.play() for all animations
- Build ideas sequentially with transformations and reveals
- Add clear, concise comments explaining each step and its purpose
- Use positional constants like UP, DOWN, LEFT, RIGHT, etc.
- Maintain balanced pacing with appropriate wait times
- Prefer Create(), Write(), Transform(), and FadeIn() for smooth motion
- Ensure no visual discontinuities (no instant jumps)
- Follow PEP8 formatting and proper indentation

Output Format:
- Start with 'from manim import *'
- Define exactly one Scene subclass
- Scene must run standalone (e.g., manim -pql filename.py ClassName)
- Do NOT wrap in markdown code blocks (no ```python or ```)
- Do NOT include any extra text or explanations outside the code
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
            
            # Remove markdown code blocks if present
            if manim_code.startswith("```python"):
                manim_code = manim_code.replace("```python", "", 1)
            if manim_code.startswith("```"):
                manim_code = manim_code.replace("```", "", 1)
            if manim_code.endswith("```"):
                manim_code = manim_code.rsplit("```", 1)[0]
            
            manim_code = manim_code.strip()

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
        video_length_text = f"- Target video length: approximately {video_length} seconds" if video_length else ""
        enhanced_prompt = f"""Educational Content: {educational_content}

Additional Requirements:
- Target difficulty level: {difficulty_level}
{video_length_text}
- Include multiple scenes if the content is complex
- Add voice-over timing comments for narration
- Use advanced Manim features where appropriate

Create a comprehensive educational video that progressively builds understanding
of the topic while maintaining the 3Blue1Brown aesthetic and teaching style.
"""

        return self.generate_manim_code(enhanced_prompt)


def generate_video(prompt: str) -> str:
    """
    Generate a Manim video file from a text prompt.

    This function takes an educational prompt, generates 3Blue1Brown-style Manim code,
    and saves it to a Python file that can be executed with Manim.

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

        # Generate the Manim code (no validation, just accept whatever is generated)
        manim_code = generator.generate_manim_code(prompt, save_to_file=False)

        # Create a filename based on the prompt
        # Clean the prompt to create a valid filename
        clean_prompt = re.sub(r'[^a-zA-Z0-9\s]', '', prompt)
        clean_prompt = re.sub(r'\s+', '_', clean_prompt.strip())
        clean_prompt = clean_prompt.lower()[:50]  # Limit length

        # Add timestamp to ensure uniqueness
        filename = f"{clean_prompt}_manim.py"

        # Create the output directory if it doesn't exist
        output_dir = "generated_videos"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Full path to the file
        file_path = os.path.join(output_dir, filename)

        # Save the code to file - accept whatever was generated
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(manim_code)

        print(f"✅ Generated Manim code saved to: {file_path}")
        return file_path

    except Exception as e:
        raise Exception(f"Error in generate_video: {str(e)}")