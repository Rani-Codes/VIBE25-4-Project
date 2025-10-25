from manim import *

class DerivativesIntro(Scene):
    def construct(self):
        # Set a dark background color for the 3Blue1Brown style
        self.camera.background_color = "#222222"

        # --- 1. Setup Axes and Function ---
        # Create the coordinate axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 9, 1],  # Adjusted y-range for f(x) = x^2
            x_length=7,
            y_length=6,         # Adjusted y-length
            axis_config={"color": GREY_A, "include_numbers": True},
        ).add_coordinates()
        # Add labels for the x and y axes
        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        # Define the function f(x) = x^2
        def func(x):
            return x**2

        # Create the graph of the function
        graph = axes.get_graph(func, x_range=[-2.5, 2.5], color=BLUE)
        # Label the function graph
        graph_label = MathTex("f(x) = x^2", color=BLUE).next_to(graph, UP, buff=0.5)

        # Create the scene title
        title = Text("Derivatives: Instantaneous Rate of Change", font_size=40).to_edge(UP)

        # Animate the creation of axes, labels, and title
        self.play(
            Create(axes),
            Write(axes_labels),
            Write(title)
        )
        # Animate the creation of the graph and its label
        self.play(Create(graph), Write(graph_label))
        self.wait(1)

        # --- 2. Define two points P and Q on the function ---
        # ValueTracker for the x-coordinate of point P (x_0)
        x_0 = ValueTracker(1.5)
        # ValueTracker for the horizontal distance between P and Q (Delta x)
        dx = ValueTracker(1.5)

        # Point P, always redrawn to follow x_0's value
        point_P = always_redraw(
            lambda: Dot(axes.c2p(x_0.get_value(), func(x_0.get_value())), color=YELLOW)
        )
        # Label for point P
        label_P = MathTex("P", color=YELLOW).next_to(point_P, LEFT, buff=0.1)

        # Point Q, always redrawn to follow x_0 + dx's value
        point_Q = always_redraw(
            lambda: Dot(axes.c2p(x_0.get_value() + dx.get_value(), func(x_0.get_value() + dx.get_value())), color=YELLOW)
        )
        # Label for point Q
        label_Q = MathTex("Q", color=YELLOW).next_to(point_Q, RIGHT, buff=0.1)

        # Vertical lines from points P and Q to the x-axis
        line_P_x = always_redraw(
            lambda: axes.get_vertical_line(point_P.get_center(), color=GREY_B)
        )
        line_Q_x = always_redraw(
            lambda: axes.get_vertical_line(point_Q.get_center(), color=GREY_B)
        )

        # Animate the creation of point P and its associated elements
        self.play(
            Create(point_P),
            Write(label_P),
            Create(line_P_x)
        )
        self.wait(0.5)
        # Animate the creation of point Q and its associated elements
        self.play(
            Create(point_Q),
            Write(label_Q),
            Create(line_Q_x)
        )
        self.wait(1)

        # --- 3. Draw the secant line connecting P and Q ---
        # The secant line, always redrawn to connect the current positions of P and Q
        secant_line = always_redraw(
            lambda: Line(point_P.get_center(), point_Q.get_center(), color=GREEN)
        )

        # Animate the creation of the secant line
        self.play(Create(secant_line))
        self.wait(1)

        # --- 4. Label Delta x and Delta f (rise and run) ---
        # Line representing Delta x
        dx_line = always_redraw(
            lambda: Line(axes.c2p(x_0.get_value(), func(x_0.get_value())),
                         axes.c2p(x_0.get_value() + dx.get_value(), func(x_0.get_value())),
                         color=RED)
        )
        # Line representing Delta f
        df_line = always_redraw(
            lambda: Line(axes.c2p(x_0.get_value() + dx.get_value(), func(x_0.get_value())),
                         axes.c2p(x_0.get_value() + dx.get_value(), func(x_0.get_value() + dx.get_value())),
                         color=RED)
        )

        # Label for Delta x, dynamically scaled and faded as dx changes
        dx_label = always_redraw(
            lambda: MathTex("\\Delta x", color=RED)
                    .next_to(dx_line, DOWN, buff=0.1)
                    .scale(dx.get_value()/1.5 * 0.7 + 0.3)  # Shrink but don't vanish
                    .set_opacity(dx.get_value()/1.5 * 0.7 + 0.3) # Fade but don't vanish
        )
        # Label for Delta f, dynamically scaled and faded as dx changes
        df_label = always_redraw(
            lambda: MathTex("\\Delta f", color=RED)
                    .next_to(df_line, RIGHT, buff=0.1)
                    .scale(dx.get_value()/1.5 * 0.7 + 0.3)
                    .set_opacity(dx.get_value()/1.5 * 0.7 + 0.3)
        )

        # Animate the creation of Delta x, Delta f lines and labels
        self.play(
            Create(dx_line),
            Create(df_line),
            Write(dx_label),
            Write(df_label)
        )
        self.wait(1)

        # --- 5. Show the slope formula for the secant line ---
        # The formula for the slope of the secant line
        slope_formula_secant = MathTex(
            "\\text{Slope} = \\frac{\\Delta f}{\\Delta x} = \\frac{f(x_0 + \\Delta x) - f(x_0)}{\\Delta x}",
            color=WHITE
        ).to_edge(DR).shift(UP*0.5).scale(0.8)

        # Animate writing the slope formula
        self.play(Write(slope_formula_secant))
        self.wait(1)

        # --- 6. Animate dx approaching zero (the limit process) ---
        # Text explaining the limit process
        explanation_text = Text("As Δx approaches 0...", font_size=30).next_to(title, DOWN).set_color(WHITE)
        self.play(Write(explanation_text))
        self.wait(0.5)

        # Animate dx decreasing from its initial value to a very small value,
        # causing Q to approach P and the secant line to rotate
        self.play(dx.animate.set_value(0.01), run_time=3, rate_func=ease_in_out_sine)
        self.wait(1)

        # --- 7. Transition to tangent line and derivative formula ---
        # Label for the tangent line, positioned relative to the secant line
        tangent_label = Text("Tangent Line", color=GREEN).next_to(secant_line, UP, buff=0.5).shift(LEFT*2)
        
        # The derivative formula, which is the limit of the secant slope
        derivative_formula = MathTex(
            "\\lim_{\\Delta x \\to 0} \\frac{\\Delta f}{\\Delta x} = \\frac{df}{dx} = f'(x_0)",
            color=YELLOW
        ).next_to(slope_formula_secant, DOWN, buff=0.5).scale(0.8)

        # Fade out the Delta x and Delta f elements, point Q, and transform the formula
        self.play(
            FadeOut(dx_line),
            FadeOut(df_line),
            FadeOut(dx_label),
            FadeOut(df_label),
            FadeOut(label_Q),
            FadeOut(line_Q_x),
            point_Q.animate.set_opacity(0), # Hide point Q as it merges with P
            ReplacementTransform(slope_formula_secant, derivative_formula) # Replace secant slope with derivative formula
        )
        self.wait(0.5)
        
        # Emphasize the secant line (now the tangent line) and add its label
        self.play(
            secant_line.animate.set_color(GREEN).set_stroke(width=5), # Thicken and keep green for tangent
            Write(tangent_label) # Show the tangent line label
        )
        self.wait(2)

        # Final explanatory text
        final_text = Text("The slope of the tangent line is the derivative at that point.", font_size=30).next_to(explanation_text, DOWN).set_color(WHITE)
        self.play(Write(final_text))
        self.wait(3)

        # --- Cleanup ---
        # Fade out all Mobjects at the end of the scene
        self.play(
            FadeOut(VGroup(axes, axes_labels, graph, graph_label, point_P, label_P, line_P_x, secant_line,
                           title, explanation_text, tangent_label, derivative_formula, final_text))
        )
        self.wait(1)