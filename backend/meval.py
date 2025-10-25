import subprocess
import os
import ast
import glob
import shutil
import uuid
import sys
from pathlib import Path
from typing import Optional, Tuple, Set


class ManimEvaluator:
    """Component for evaluating and rendering Manim Python code."""
    
    def __init__(
        self, 
        output_dir: Optional[str] = None,
        media_dir: Optional[str] = None,
        base_url: str = "http://localhost:8000"
    ):
        """
        Initialize the Manim evaluator.
        
        Args:
            output_dir: Optional custom output directory for videos.
                       If None, uses Manim's default (media/videos/).
            media_dir: Directory to store served videos with UUID filenames.
                      If None, uses './media' in current directory.
            base_url: Base URL for serving videos (default: http://localhost:8000).
        """
        self.output_dir = output_dir
        self.media_dir = media_dir or os.path.join(os.getcwd(), "media")
        self.base_url = base_url.rstrip('/')
        
        # Create media directory if it doesn't exist
        os.makedirs(self.media_dir, exist_ok=True)
    
    def extract_plugin_imports(self, filepath: str) -> Set[str]:
        """
        Extract Manim plugin imports from a Python file.
        
        Args:
            filepath: Path to the Python file.
            
        Returns:
            Set of plugin package names that need to be installed.
        """
        if not os.path.exists(filepath):
            return set()
        
        with open(filepath, 'r') as f:
            code = f.read()
        
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return set()
        
        plugins = set()
        
        for node in ast.walk(tree):
            # Handle: import manim_slides
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith('manim_'):
                        plugins.add(alias.name)
            
            # Handle: from manim_physics import *
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith('manim_'):
                    # Extract the base package name
                    base_package = node.module.split('.')[0]
                    plugins.add(base_package)
        
        return plugins
    
    def install_plugins(self, plugins: Set[str]) -> None:
        """
        Install Manim plugins using pip.
        
        Args:
            plugins: Set of plugin package names to install (with underscores).
        
        Note:
            Manim plugins use hyphens on PyPI (manim-chemistry) but underscores
            in imports (manim_chemistry). This method handles the conversion.
        """
        if not plugins:
            return
        
        for plugin in plugins:
            # Convert underscores to hyphens for PyPI package name
            # e.g., manim_chemistry -> manim-chemistry
            pypi_name = plugin.replace('_', '-')
            
            print(f"Installing Manim plugin: {pypi_name}")
            try:
                # Check if already installed (try both names)
                for name in [plugin, pypi_name]:
                    result = subprocess.run(
                        [sys.executable, "-m", "pip", "show", name],
                        capture_output=True,
                        text=True
                    )
                    
                    if result.returncode == 0:
                        print(f"  ✓ {pypi_name} already installed")
                        break
                else:
                    # Not installed, try to install using hyphenated PyPI name
                    result = subprocess.run(
                        [sys.executable, "-m", "pip", "install", pypi_name],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    print(f"  ✓ {pypi_name} installed successfully")
                
            except subprocess.CalledProcessError as e:
                # Try with underscore name as fallback
                try:
                    print(f"  Retrying with alternative name: {plugin}")
                    result = subprocess.run(
                        [sys.executable, "-m", "pip", "install", plugin],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    print(f"  ✓ {plugin} installed successfully")
                except subprocess.CalledProcessError:
                    print(f"  ✗ Failed to install {pypi_name}: {e.stderr}")
                    # Continue anyway - the render might still work
    
    def extract_scene_classes(self, filepath: str) -> list[str]:
        """
        Extract all Scene class names from a Python file.
        
        Args:
            filepath: Path to the Python file containing Manim code.
            
        Returns:
            List of Scene class names found in the file.
            
        Raises:
            FileNotFoundError: If the file doesn't exist.
            SyntaxError: If the Python file has syntax errors.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        with open(filepath, 'r') as f:
            code = f.read()
        
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            raise SyntaxError(f"Syntax error in {filepath}: {e}")
        
        scene_classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check if class inherits from Scene or its subclasses
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        # All Manim scene types from documentation
                        if base.id in [
                            'Scene',                    # Basic canvas for animations
                            'ThreeDScene',              # 3D objects and animations
                            'MovingCameraScene',        # Camera can be moved around
                            'ZoomedScene',              # Supports zooming on sections
                            'VectorSpaceScene',         # Suitable for vector spaces
                            'LinearTransformationScene',# Linear transformation animations
                            'Section',                  # Building blocks of segmented video API
                        ]:
                            scene_classes.append(node.name)
                            break
        
        return scene_classes
    
    def render_manim(
        self, 
        filepath: str, 
        scene_name: Optional[str] = None,
        quality: str = "l",  # l=low, m=medium, h=high, k=4k
        preview: bool = False
    ) -> Tuple[str, str]:
        """
        Render a Manim animation from a Python file.
        
        Args:
            filepath: Path to the Python file containing Manim code.
            scene_name: Name of the Scene class to render. 
                       If None, will use the first Scene class found.
            quality: Video quality flag (l=480p15, m=720p30, h=1080p60, k=2160p60).
            preview: Whether to open the video after rendering.
            
        Returns:
            Tuple of (video_path, scene_name_used)
            
        Raises:
            ValueError: If no Scene classes found or specified scene doesn't exist.
            RuntimeError: If manim rendering fails.
        """
        # Validate filepath
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        # Detect and install any required plugins
        plugins = self.extract_plugin_imports(filepath)
        if plugins:
            print(f"Detected Manim plugins: {', '.join(plugins)}")
            self.install_plugins(plugins)
        
        # Extract scene classes if scene_name not provided
        if scene_name is None:
            scene_classes = self.extract_scene_classes(filepath)
            if not scene_classes:
                raise ValueError(f"No Scene classes found in {filepath}")
            scene_name = scene_classes[0]
            print(f"Auto-detected scene class: {scene_name}")
        
        # Build manim command
        cmd = ["manim"]
        
        # Add quality flag
        if preview:
            cmd.append("-p")
        cmd.append(f"-q{quality}")
        
        # Add output directory if specified
        if self.output_dir:
            cmd.extend(["--media_dir", self.output_dir])
        
        # Add file and scene name
        cmd.extend([filepath, scene_name])
        
        print(f"Running command: {' '.join(cmd)}")
        
        # Execute manim command
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            print("Manim output:")
            print(result.stdout)
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Manim rendering failed:\n{e.stderr}"
            raise RuntimeError(error_msg)
        
        # Find the generated video file
        video_path = self._find_video_output(filepath, scene_name, quality)
        
        if not video_path or not os.path.exists(video_path):
            raise RuntimeError(f"Video file not found after rendering")
        
        return video_path, scene_name
    
    def _find_video_output(
        self, 
        source_file: str, 
        scene_name: str,
        quality: str
    ) -> Optional[str]:
        """
        Find the generated video file path based on Manim's output structure.
        
        Args:
            source_file: Original Python source file path.
            scene_name: Name of the rendered scene.
            quality: Quality setting used for rendering.
            
        Returns:
            Path to the video file, or None if not found.
        """
        # Get the base filename without extension
        base_name = Path(source_file).stem
        
        # Determine quality folder name
        quality_map = {
            'l': '480p15',
            'm': '720p30', 
            'h': '1080p60',
            'k': '2160p60'
        }
        quality_folder = quality_map.get(quality, '480p15')
        
        # Determine base directory
        if self.output_dir:
            base_dir = self.output_dir
        else:
            # Default Manim output structure
            source_dir = os.path.dirname(os.path.abspath(source_file))
            base_dir = os.path.join(source_dir, "media")
        
        # Build expected path
        video_dir = os.path.join(base_dir, "videos", base_name, quality_folder)
        
        # Look for video files (mp4 by default)
        if os.path.exists(video_dir):
            video_files = glob.glob(os.path.join(video_dir, f"{scene_name}.mp4"))
            if video_files:
                return video_files[0]
        
        # Fallback: search more broadly
        search_pattern = os.path.join(base_dir, "**", f"{scene_name}.mp4")
        video_files = glob.glob(search_pattern, recursive=True)
        
        return video_files[0] if video_files else None
    
    def evaluate(self, filepath: str, **kwargs) -> str:
        """
        Main evaluation method - render Manim code and return video URL.
        
        Args:
            filepath: Path to the Python file containing Manim code.
            **kwargs: Additional arguments passed to render_manim().
            
        Returns:
            URL to the generated video file (e.g., http://localhost:8000/media/uuid.mp4).
        """
        video_path, scene_name = self.render_manim(filepath, **kwargs)
        print(f"Successfully rendered scene '{scene_name}'")
        print(f"Video saved to: {video_path}")
        
        # Generate unique filename with UUID
        unique_id = str(uuid.uuid4())
        new_filename = f"{unique_id}.mp4"
        destination_path = os.path.join(self.media_dir, new_filename)
        
        # Copy video to media directory
        shutil.copy2(video_path, destination_path)
        print(f"Copied to: {destination_path}")
        
        # Generate URL
        video_url = f"{self.base_url}/media/{new_filename}"
        print(f"Video URL: {video_url}")
        
        return video_url


# Global evaluator instance
_evaluator = None


def _get_evaluator() -> ManimEvaluator:
    """Get or create the global ManimEvaluator instance."""
    global _evaluator
    if _evaluator is None:
        # Set media directory relative to this file
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        media_dir = os.path.join(backend_dir, "media")
        _evaluator = ManimEvaluator(
            media_dir=media_dir,
            base_url="http://localhost:8000"
        )
    return _evaluator


def eval_file(filepath: str) -> str:
    """
    Evaluate a Manim file and return the video URL.
    
    This is the main entry point for rendering Manim animations.
    It handles everything: rendering, copying to media directory,
    and generating a unique URL.
    
    Args:
        filepath: Path to the Python file containing Manim code.
                 Can be relative or absolute path.
        
    Returns:
        URL to the generated video file (e.g., http://localhost:8000/media/{uuid}.mp4).
        
    Example:
        >>> video_url = eval_file("test.py")
        >>> print(f"Video URL: {video_url}")
        
    Raises:
        FileNotFoundError: If the file doesn't exist.
        ValueError: If no Scene classes found in the file.
        RuntimeError: If manim rendering fails.
    """
    evaluator = _get_evaluator()
    
    # Make filepath absolute if it's relative
    if not os.path.isabs(filepath):
        # Assume relative to backend directory
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(backend_dir, filepath)
    
    return evaluator.evaluate(filepath, quality="h")


# Convenience function for simple usage (backward compatibility)
def evaluate_manim_code(filepath: str, scene_name: Optional[str] = None) -> str:
    """
    Evaluate Manim code from a file and return the video URL.
    
    Args:
        filepath: Path to the Python file containing Manim code.
        scene_name: Optional name of the Scene class to render.
        
    Returns:
        URL to the generated video file (e.g., http://localhost:8000/media/uuid.mp4).
        
    Example:
        >>> video_url = evaluate_manim_code("quadratic_manim.py")
        >>> print(f"Video URL: {video_url}")
    """
    evaluator = _get_evaluator()
    return evaluator.evaluate(filepath, scene_name=scene_name)


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        
        try:
            video_url = eval_file(filepath)
            print(f"\n✓ Success! Video URL: {video_url}")
        except Exception as e:
            print(f"\n✗ Error: {e}")
            sys.exit(1)
    else:
        print("Usage: python meval.py <filepath>")
        print("\nExample:")
        print("  python meval.py test.py")
        print("  python meval.py quadratic_manim.py")

