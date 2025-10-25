from manim import *

class IntegralConcept(Scene):
    def construct(self):
        # Set up the scene with a dark background (default for Manim)
        # and a title.
        title = Text("The Integral: Area Under a Curve", font_size=48, color=WHITE)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title, shift=UP))

        # --- 1. Create Axes and Function ---
        # Define the axes for the graph.
        axes = Axes(
            x_range=[-0.5, 3.5, 1],  # x from -0.5 to 3.5, with ticks every 1 unit
            y_range=[-0.5, 9.5, 1],  # y from -0.5 to 9.5, with ticks every 1 unit
            x_length=7,
            y_length=6,
            axis_config={"color": GRAY},
            tips=False, # No arrows at the end of axes
        )
        # Add labels to the axes.
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("f(x)")
        axes_labels = VGroup(x_label, y_label)

        # Define the function f(x) = x^2.
        def func(x):
            return x**2

        graph = axes.get_graph(func, x_range=[0, 3], color=BLUE) # Graph from x=0 to x=3

        # Label the function.
        func_label = MathTex("f(x) = x^2", color=BLUE).next_to(graph, UP + RIGHT, buff=0.2)

        # Animate the creation of axes, graph, and labels.
        self.play(Create(axes), Create(axes_labels))
        self.play(Create(graph), Write(func_label))
        self.wait(1)

        # --- 2. Approximating with Rectangles (Riemann Sums) ---
        # Define the integration interval [a, b].
        a = 0.5
        b = 2.5

        # Create vertical lines at a and b.
        a_line = axes.get_vertical_line(axes.input_to_graph_point(a, graph), color=RED)
        b_line = axes.get_vertical_line(axes.input_to_graph_point(b, graph), color=RED)

        # Create labels for a and b.
        a_label_text = MathTex("a", color=RED).next_to(a_line, DOWN, buff=0.1)
        b_label_text = MathTex("b", color=RED).next_to(b_line, DOWN, buff=0.1)

        self.play(
            Create(a_line), Write(a_label_text),
            Create(b_line), Write(b_label_text)
        )
        self.wait(0.5)

        # Text to introduce Riemann sums.
        rect_text = Text("Approximating area with rectangles", font_size=30).to_edge(UP)
        self.play(Write(rect_text))
        self.wait(0.5)

        # Create 4 rectangles (left Riemann sum).
        rects1 = axes.get_riemann_rectangles(
            graph=graph,
            x_range=[a, b],
            dx=(b-a)/4, # Width of each rectangle
            stroke_width=0.1,
            stroke_color=YELLOW,
            fill_opacity=0.6,
            color=YELLOW,
            input_sample_type="left" # Left Riemann sum
        )
        self.play(Create(rects1))
        self.wait(1)

        # Increase the number of rectangles to 10.
        rects2 = axes.get_riemann_rectangles(
            graph=graph,
            x_range=[a, b],
            dx=(b-a)/10,
            stroke_width=0.1,
            stroke_color=YELLOW,
            fill_opacity=0.6,
            color=YELLOW,
            input_sample_type="left"
        )
        self.play(Transform(rects1, rects2)) # Transform from 4 to 10 rectangles
        self.wait(1)

        # Increase the number of rectangles to 20.
        rects3 = axes.get_riemann_rectangles(
            graph=graph,
            x_range=[a, b],
            dx=(b-a)/20,
            stroke_width=0.1,
            stroke_color=YELLOW,
            fill_opacity=0.6,
            color=YELLOW,
            input_sample_type="left"
        )
        self.play(Transform(rects1, rects3)) # Transform from 10 to 20 rectangles
        self.wait(1)

        # --- 3. Transition to Smooth Area (The Limit) ---
        # Text for the limit concept.
        limit_text = Text("As the number of rectangles approaches infinity...", font_size=30).to_edge(UP)
        self.play(Transform(rect_text, limit_text))
        self.wait(1)

        # Remove the rectangles.
        self.play(FadeOut(rects1))

        # Fill the area under the curve from a to b.
        area_under_curve = axes.get_area(
            graph=graph,
            x_range=[a, b],
            color=TEAL,
            opacity=0.7
        )
        self.play(Create(area_under_curve)) # Animate filling the area
        self.wait(1)

        # Update the text.
        exact_area_text = Text("The exact area under the curve is the integral.", font_size=30).to_edge(UP)
        self.play(Transform(rect_text, exact_area_text))
        self.wait(1)

        # --- 4. Integral Notation ---
        # Define the integral notation.
        integral_notation = MathTex(
            "\\int_{a}^{b} f(x) \\, dx",
            font_size=60,
            color=WHITE
        ).next_to(axes, DOWN, buff=1.0) # Position below the axes

        # Animate the creation of the integral notation.
        self.play(Write(integral_notation))
        self.wait(1)

        # Highlight different parts of the integral.
        # Highlight f(x).
        self.play(
            graph.animate.set_stroke(width=6, color=YELLOW),
            func_label.animate.set_color(YELLOW),
            integral_notation[3].animate.set_color(YELLOW), # f(x) part
            run_time=1
        )
        self.wait(0.5)
        self.play(
            graph.animate.set_stroke(width=4, color=BLUE),
            func_label.animate.set_color(BLUE),
            integral_notation[3].animate.set_color(WHITE),
            run_time=0.5
        )

        # Highlight a and b.
        self.play(
            a_line.animate.set_color(YELLOW),
            b_line.animate.set_color(YELLOW),
            a_label_text.animate.set_color(YELLOW),
            b_label_text.animate.set_color(YELLOW),
            integral_notation[1].animate.set_color(YELLOW), # a part
            integral_notation[2].animate.set_color(YELLOW), # b part
            run_time=1
        )
        self.wait(0.5)
        self.play(
            a_line.animate.set_color(RED),
            b_line.animate.set_color(RED),
            a_label_text.animate.set_color(RED),
            b_label_text.animate.set_color(RED),
            integral_notation[1].animate.set_color(WHITE),
            integral_notation[2].animate.set_color(WHITE),
            run_time=0.5
        )
        self.wait(2)

        # Clean up the scene.
        self.play(
            FadeOut(rect_text),
            FadeOut(integral_notation),
            FadeOut(area_under_curve),
            FadeOut(a_line), FadeOut(b_line),
            FadeOut(a_label_text), FadeOut(b_label_text),
            FadeOut(func_label),
            FadeOut(graph),
            FadeOut(axes),
            FadeOut(axes_labels)
        )
        self.wait(1)