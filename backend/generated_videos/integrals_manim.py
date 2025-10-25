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

        f = lambda x: 0.4*x**2 + 1
        graph = ax.plot(f, x_range=[0, 4.8], color=BLUE)
        f_label = MathTex("f(x)").set_color(BLUE).scale(0.8)
        f_label.next_to(graph.points[-1], UR, buff=0.2)
        self.play(Create(graph), FadeIn(f_label, shift=0.2*UP))
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

        # Replace rectangles with true filled area
        self.play(FadeOut(rects_coarse, run_time=0.8))
        self.play(shaded.animate.set_opacity(0.45))
        self.wait(0.5)

        # Indefinite integral as "antiderivative"
        indef = VGroup(
            MathTex(r"\textbf{Indefinite integral:}~~\int f(x)\,dx = F(x) + C"),
            MathTex(r"\text{where } F'(x)=f(x)\,\,\text{ (an antiderivative).}")
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.6)
        indef.next_to(expl, DOWN, buff=0.5).align_to(expl, LEFT)
        self.play(Write(indef[0]))
        self.play(Write(indef[1]))
        self.wait(0.6)

        # Fundamental Theorem of Calculus (Part 2 evaluation)
        ftc2 = MathTex(
            r"\int_{0}^{4} f(x)\,dx = F(4)-F(0)"
        ).scale(0.7).next_to(eq_sum, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(ftc2))
        self.wait(0.6)

        # Accumulation function A(x) = ∫_0^x f(t)dt
        track = ValueTracker(0.0)

        def get_area_to_x():
            x_val = track.get_value()
            return ax.get_area(graph, x_range=(0, x_val), color=GREEN, opacity=0.45)

        area_to_x = always_redraw(get_area_to_x)

        moving_x_line = always_redraw(lambda:
            ax.get_vertical_line(
                ax.c2p(track.get_value(), f(track.get_value())),
                color=GREEN
            )
        )
        moving_dot = always_redraw(lambda:
            Dot(ax.c2p(track.get_value(), f(track.get_value())), radius=0.06, color=GREEN)
        )

        A_def = MathTex(
            r"A(x)=\int_{0}^{x} f(t)\,dt"
        ).scale(0.7).to_corner(UR).shift(0.2*LEFT + 0.2*DOWN)
        self.play(Write(A_def))

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
