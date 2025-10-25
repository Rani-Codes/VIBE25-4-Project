from manim import *

class VariableIntroduction(Scene):
    def construct(self):
        # 1. Introduce the concept of a variable 'x'
        # Display 'x' in a distinct color to represent its identity.
        x_symbol_initial = MathTex("x", color=BLUE)
        self.play(Write(x_symbol_initial))
        self.wait(0.5)

        # 2. Define the value of 'x': x = 5
        # Create a VGroup for the equation components to maintain layout and transform 'x_symbol_initial' into the 'x' part.
        x_equation_parts = VGroup(
            MathTex("x", color=BLUE),
            MathTex("=", color=WHITE),
            MathTex("5", color=YELLOW)
        ).arrange(RIGHT, buff=0.1).to_edge(UP)

        # Transform the initial 'x' into the 'x' component of the equation.
        self.play(Transform(x_symbol_initial, x_equation_parts[0]))
        # Write the rest of the equation "= 5".
        self.play(Write(x_equation_parts[1:]))
        self.wait(0.7)

        # 3. Create a visual representation of 'x' as a bar
        # A rectangle whose length represents the value of x, colored blue.
        x_value_rect = Rectangle(width=5, height=0.8, color=BLUE, fill_opacity=0.8)
        x_value_label = MathTex("x", color=BLUE).next_to(x_value_rect, UP)
        five_label = MathTex("5", color=YELLOW).next_to(x_value_rect, DOWN)

        # Group these visual elements for easier positioning and animation.
        x_visual_group = VGroup(x_value_rect, x_value_label, five_label).shift(LEFT * 2)

        # Fade in the visual representation.
        self.play(FadeIn(x_visual_group))
        self.wait(1)

        # 4. Introduce an operation: x + 2
        # Display the operation below the initial equation, matching 'x' and '2' colors.
        operation_text_group = VGroup(
            MathTex("x", color=BLUE),
            MathTex("+", color=WHITE),
            MathTex("2", color=YELLOW)
        ).arrange(RIGHT, buff=0.1).next_to(x_equation_parts, DOWN, buff=0.8)

        self.play(Write(operation_text_group))
        self.wait(0.7)

        # 5. Animate the operation: Visually add '2' to 'x'
        # Create another rectangle representing '2', colored yellow, and place it next to the 'x' rectangle.
        plus_rect = Rectangle(width=2, height=0.8, color=YELLOW, fill_opacity=0.8).next_to(x_value_rect, RIGHT, buff=0)
        plus_label = MathTex("2", color=YELLOW).next_to(plus_rect, DOWN)

        # Animate the creation of the '+2' visual.
        self.play(Create(plus_rect), Write(plus_label))
        self.wait(0.7)

        # 6. Show the combined result: x + 2 = 7
        # Create the full result equation, with the final '7' in green.
        result_equation_group = VGroup(
            MathTex("x", color=BLUE),
            MathTex("+", color=WHITE),
            MathTex("2", color=YELLOW),
            MathTex("=", color=WHITE),
            MathTex("7", color=GREEN)
        ).arrange(RIGHT, buff=0.1).next_to(x_equation_parts, DOWN, buff=0.8)

        # Use TransformMatchingTex to smoothly transform "x + 2" into "x + 2 = 7".
        self.play(
            TransformMatchingTex(operation_text_group, result_equation_group)
        )
        self.wait(1)

        # 7. Final visual: Show the combined rectangle labeled '7'
        # Create a single new rectangle representing the total length (7 units), colored green.
        total_rect = Rectangle(width=7, height=0.8, color=GREEN, fill_opacity=0.8).move_to(x_value_rect.get_center() + RIGHT * 1)
        total_label = MathTex("7", color=GREEN).next_to(total_rect, DOWN)

        # Transform the individual rectangles into the single combined rectangle.
        # Fade out the old labels and write the new total label.
        self.play(
            Transform(x_value_rect, total_rect),
            Transform(plus_rect, total_rect),
            FadeOut(x_value_label),
            FadeOut(five_label),
            FadeOut(plus_label),
            Write(total_label)
        )
        self.wait(2)

        # Clean up the scene by fading out all elements.
        self.play(
            FadeOut(x_symbol_initial),
            FadeOut(x_equation_parts[1:]),
            FadeOut(result_equation_group),
            FadeOut(total_rect),
            FadeOut(total_label)
        )
        self.wait(0.5)