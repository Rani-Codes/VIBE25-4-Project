from manim import *

class VectorAddition(Scene):
    def construct(self):
        # --- Configuration and Initial Setup ---
        # Set colors for the vectors
        color_a = BLUE_A
        color_b = RED_A
        color_sum = YELLOW_A

        # Title
        title = Text("Vector Addition", font_size=60).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create a coordinate plane for context
        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            x_length=12,
            y_length=8,
            axis_config={"include_numbers": False},
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_opacity": 0.5,
            }
        ).add_coordinates()
        self.play(Create(plane, run_time=1.5))
        self.wait(0.5)

        # --- Define and Animate Vector A ---
        # Vector A will go from origin to (3, 2)
        vec_a_coords = [3, 2, 0]
        vector_a = Vector(vec_a_coords, color=color_a)
        label_a = MathTex(r"\vec{A}", color=color_a).next_to(vector_a.get_end(), RIGHT + UP)

        self.play(GrowArrow(vector_a))
        self.play(Write(label_a))
        self.wait(1)

        # --- Define and Animate Vector B ---
        # Vector B will go from origin to (-1, 3)
        vec_b_coords = [-1, 3, 0]
        vector_b = Vector(vec_b_coords, color=color_b)
        label_b = MathTex(r"\vec{B}", color=color_b).next_to(vector_b.get_end(), LEFT + UP)

        self.play(GrowArrow(vector_b))
        self.play(Write(label_b))
        self.wait(1)

        # --- Introduce the concept of addition ---
        addition_text = Text("How do we add vectors A and B?", font_size=36).next_to(title, DOWN)
        self.play(Write(addition_text))
        self.wait(1.5)

        # --- Head-to-Tail Method Explanation ---
        # Duplicate vector B to show its translation
        vector_b_translated = vector_b.copy().set_color(color_b)
        label_b_translated = label_b.copy().set_color(color_b)

        # Animate moving vector B
        self.play(
            Transform(addition_text, Text("Place the tail of B at the head of A.", font_size=36).next_to(title, DOWN)),
            vector_b_translated.animate.shift(vector_a.get_end()),
            label_b_translated.animate.shift(vector_a.get_end()),
            run_time=2
        )
        self.wait(1)

        # --- Show the resultant vector ---
        # The sum vector goes from the origin to the end of the translated B
        sum_coords = [
            vec_a_coords[0] + vec_b_coords[0],
            vec_a_coords[1] + vec_b_coords[1],
            0
        ]
        vector_sum = Vector(sum_coords, color=color_sum)
        label_sum = MathTex(r"\vec{A} + \vec{B}", color=color_sum).next_to(vector_sum.get_end(), RIGHT)

        self.play(
            Transform(addition_text, Text("The resultant vector goes from the start of A to the end of B.", font_size=36).next_to(title, DOWN)),
            GrowArrow(vector_sum),
            Write(label_sum),
            run_time=2
        )
        self.wait(2)

        # --- Parallelogram Rule (optional, but good for completeness) ---
        self.play(
            Transform(addition_text, Text("This is also known as the parallelogram rule.", font_size=36).next_to(title, DOWN)),
            FadeOut(label_b_translated, shift=UP),
            FadeOut(vector_b_translated, shift=UP),
            FadeIn(vector_b), # Bring original B back
            FadeIn(label_b),  # Bring original B label back
            run_time=1.5
        )
        self.wait(0.5)

        # Create a duplicate of vector A to form the other side of the parallelogram
        vector_a_translated = vector_a.copy().set_color(color_a).set_opacity(0.5)
        self.play(
            vector_a_translated.animate.shift(vector_b.get_end()),
            run_time=1.5
        )
        self.wait(1)

        # Fade out temporary elements and keep the core idea
        self.play(
            FadeOut(addition_text),
            FadeOut(title),
            FadeOut(vector_a_translated),
            run_out=1.5
        )
        self.wait(1)