from manim import *

class IntegralConcepts(Scene):
    def construct(self):
        # Title
        title = Text("Integrals: area, accumulation, and the Fundamental Theorem", weight=BOLD).scale(0.6)
        self.play(FadeIn(title, shift=DOWN))
        self.wait(0.7)
        self.play(title.animate.to_edge(UP))
        # Axes and function
        ax = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 8, 1],
            x_length=8,
            y_length=4.5,
            tips=False
        )
        ax.to_edge(DOWN)
        labels = ax.get_axis_labels(MathTex("x"), MathTex("y"))
        self.play(Create(ax), FadeIn(labels, shift=0.2*UP))

        # Define the function f(x) = x^2.
        def func(x):
            return x**2

        graph = axes.plot(func, x_range=[0, 3], color=BLUE) # Graph from x=0 to x=3

        # Label the function.
        func_label = Text("f(x) = x²", font_size=32, color=BLUE).next_to(graph, UP + RIGHT, buff=0.2)

        # Animate the creation of axes, graph, and labels.
        self.play(Create(axes), Create(axes_labels))
        self.play(Create(graph), Write(func_label))
        self.wait(1)

        # --- 2. Approximating with Rectangles (Riemann Sums) ---
        # Define the integration interval [a, b].
        a = 0.5
        b = 2.5

        # Create vertical lines at a and b.
        a_line = axes.get_vertical_line(axes.i2gp(a, graph), color=RED)
        b_line = axes.get_vertical_line(axes.i2gp(b, graph), color=RED)

        # Create labels for a and b.
        a_label_text = Text("a", font_size=28, color=RED).next_to(a_line, DOWN, buff=0.1)
        b_label_text = Text("b", font_size=28, color=RED).next_to(b_line, DOWN, buff=0.1)

        self.play(
            Create(a_line), Write(a_label_text),
            Create(b_line), Write(b_label_text)
        )
        self.wait(0.5)

        # Area under the curve (definite integral idea)
        a, b = 0, 4
        shaded = ax.get_area(graph, x_range=(a, b), color=BLUE, opacity=0.35, bounded_graph=ax.get_graph(lambda x: 0))
        bracket = Brace(shaded, DOWN, buff=0.1, color=BLUE)
        area_text = bracket.get_text("Area under \(f(x)\) from \(x=0\) to \(x=4\)").scale(0.5)
        self.play(FadeIn(shaded), GrowFromCenter(bracket), FadeIn(area_text))
        self.wait(0.7)

        # Riemann sums: rectangles approximation
        expl = VGroup(
            MathTex(r"\textbf{Idea: } \int_{0}^{4} f(x)\,dx \approx \sum_{i=1}^{n} f(x_i)\,\Delta x"),
            MathTex(r"\text{as } n \uparrow,\ \Delta x \downarrow,\ \text{sum } \to \text{ area}")
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.6)
        expl.to_corner(UR).shift(0.2*LEFT + 0.2*DOWN)
        self.play(Write(expl[0]))
        self.wait(0.3)
        self.play(Write(expl[1]))

        def riemann_rects(n, method="left", color=YELLOW):
            dx = (b - a)/n
            rects = VGroup()
            for i in range(n):
                x_left = a + i*dx
                if method == "left":
                    sample = x_left
                elif method == "mid":
                    sample = x_left + dx/2
                else:
                    sample = x_left + dx
                h = max(0, f(sample))
                p0 = ax.c2p(x_left, 0)
                p1 = ax.c2p(x_left+dx, 0)
                p2 = ax.c2p(x_left+dx, h)
                p3 = ax.c2p(x_left, h)
                rect = Polygon(p0, p1, p2, p3, color=color, fill_opacity=0.35, stroke_width=1.5)
                rects.add(rect)
            return rects

        rects_coarse = riemann_rects(6, method="left", color=YELLOW)
        rects_med = riemann_rects(12, method="left", color=YELLOW)
        rects_fine = riemann_rects(30, method="left", color=YELLOW)

        self.play(FadeIn(rects_coarse, lag_ratio=0.05, run_time=1.2))
        self.wait(0.4)
        self.play(Transform(rects_coarse, rects_med, run_time=1.0))
        self.play(Transform(rects_coarse, rects_fine, run_time=1.0))
        self.wait(0.5)

        # From sum to exact area (limit definition)
        eq_sum = MathTex(
            r"\int_{0}^{4} f(x)\,dx = \lim_{n\to\infty}\sum_{i=1}^{n} f(x_i)\,\Delta x"
        ).scale(0.7).to_corner(UL).shift(0.2*RIGHT + 0.2*DOWN)
        box = SurroundingRectangle(eq_sum, color=YELLOW, buff=0.15)
        self.play(Write(eq_sum), Create(box))
        self.wait(0.7)

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
        # Define the integral notation using Text (Unicode integral symbol).
        integral_notation = Text(
            "∫ᵇₐ f(x) dx",
            font_size=48,
            color=WHITE
        ).next_to(axes, DOWN, buff=1.0) # Position below the axes

        # Animate the creation of the integral notation.
        self.play(Write(integral_notation))
        self.wait(1)

        # Highlight f(x) part of the integral.
        self.play(
            graph.animate.set_stroke(width=6, color=YELLOW),
            func_label.animate.set_color(YELLOW),
            integral_notation.animate.set_color(YELLOW),
            run_time=1
        )
        self.wait(0.5)
        self.play(
            graph.animate.set_stroke(width=4, color=BLUE),
            func_label.animate.set_color(BLUE),
            integral_notation.animate.set_color(WHITE),
            run_time=0.5
        )

        # Highlight a and b bounds.
        self.play(
            a_line.animate.set_color(YELLOW),
            b_line.animate.set_color(YELLOW),
            a_label_text.animate.set_color(YELLOW),
            b_label_text.animate.set_color(YELLOW),
            run_time=1
        )
        self.wait(0.5)
        self.play(
            a_line.animate.set_color(RED),
            b_line.animate.set_color(RED),
            a_label_text.animate.set_color(RED),
            b_label_text.animate.set_color(RED),
            run_time=0.5
        )
        self.wait(2)

        self.play(FadeOut(bracket), FadeOut(area_text))
        self.add(area_to_x, moving_x_line, moving_dot)
        self.play(track.animate.set_value(4.0), run_time=3, rate_func=smooth)
        self.wait(0.4)

        # Fundamental Theorem of Calculus (Part 1 derivative of accumulation)
        ftc1 = MathTex(
            r"\frac{d}{dx}\left[\int_{0}^{x} f(t)\,dt\right] = f(x)"
        ).scale(0.7).next_to(A_def, DOWN, aligned_edge=LEFT, buff=0.35).set_color(GREEN)
        self.play(Write(ftc1))
        self.wait(0.6)

        # Visual cue: compare slope of A(x) vs height of f(x)
        # Sketch A(x) numerically via samples for intuition
        samples = 60
        xs = np.linspace(0, 4, samples)
        # approximate A(x) with cumulative trapezoid
        vals = [0]
        for i in range(1, samples):
            x0, x1 = xs[i-1], xs[i]
            vals.append(vals[-1] + 0.5*(f(x0)+f(x1))*(x1-x0))
        A_points = [ax.c2p(x, np.interp(x, xs, vals)) for x in xs]
        A_graph = VMobject(color=PURPLE)
        A_graph.set_points_smoothly([*A_points])
        A_label = MathTex("A(x)").set_color(PURPLE).scale(0.8)
        A_label.next_to(A_points[-1], UL, buff=0.15)

        self.play(Create(A_graph), FadeIn(A_label, shift=UP))
        self.wait(0.3)

        # Move along x again to emphasize "slope of A equals height of f"
        hl = VGroup(
            Arrow(A_graph.point_from_proportion(0.55), A_graph.point_from_proportion(0.60), buff=0, stroke_width=3),
            Arrow(ax.c2p(3.2, 0.0), ax.c2p(3.2, f(3.2)), buff=0, stroke_width=3, color=BLUE)
        )
        self.play(Flash(A_graph.point_from_proportion(0.6), color=PURPLE, line_length=0.3),
                  Flash(ax.c2p(3.2, f(3.2)), color=BLUE, line_length=0.3))
        self.play(Create(hl), run_time=0.8)
        note = MathTex(r"\text{slope of }A \; \leftrightarrow \; f(x)").scale(0.6)
        note.next_to(ftc1, DOWN, aligned_edge=LEFT, buff=0.25)
        self.play(Write(note))
        self.wait(0.8)

        # Clean up and final summary panel
        self.play(*map(FadeOut, [hl, note, A_graph, A_label, area_to_x, moving_x_line, moving_dot]))
        summary = VGroup(
            MathTex(r"\int_{a}^{b} f(x)\,dx \;=\; \lim_{n\to\infty}\sum f(x_i)\,\Delta x \;=\; F(b)-F(a)"),
            MathTex(r"A(x)=\int_{a}^{x} f(t)\,dt \;\Rightarrow\; A'(x)=f(x)")
        ).arrange(DOWN, buff=0.3).scale(0.8)
        summary.to_edge(LEFT).shift(0.3*RIGHT + 0.2*UP)

        # Keep original area as context
        final_area = ax.get_area(graph, x_range=(a, b), color=BLUE, opacity=0.35)
        self.play(FadeIn(final_area))
        self.play(Write(summary[0]))
        self.play(Write(summary[1]))
        self.wait(1.2)

        # Closing
        box2 = SurroundingRectangle(summary, color=ORANGE, buff=0.2)
        self.play(Create(box2))
        self.wait(1.0)
        self.play(*map(FadeOut, [box2, final_area, eq_sum, ftc2, expl, indef, A_def, ftc1, shaded, graph, f_label, labels, ax]))
        thanks = Text("Integral = area + accumulation", weight=BOLD).set_color(YELLOW).scale(0.8)
        self.play(FadeIn(thanks, shift=0.3*UP))
        self.wait(1.0)
        self.play(FadeOut(thanks), FadeOut(title))
