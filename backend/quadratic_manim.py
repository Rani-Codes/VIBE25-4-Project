from manim import *

class QuadraticEquation(Scene):
    def construct(self):
        # Title
        title = Text("The Quadratic Equation", font_size=48)
        self.play(Write(title))
        self.wait()
        self.play(title.animate.to_edge(UP))

        # Standard form using Tex (simpler, less likely to fail)
        standard_form = Tex(
            r"ax$^2$ + bx + c = 0",
            font_size=44
        )
        standard_form.next_to(title, DOWN, buff=0.5)
        self.play(Write(standard_form))
        self.wait()

        # Description
        desc = Text("where a ≠ 0", font_size=32, color=YELLOW)
        desc.next_to(standard_form, DOWN, buff=0.3)
        self.play(FadeIn(desc))
        self.wait(2)

        # Clear for formula
        self.play(
            FadeOut(standard_form),
            FadeOut(desc)
        )

        # The quadratic formula
        formula_text = Text("The Quadratic Formula:", font_size=36)
        formula_text.next_to(title, DOWN, buff=0.5)
        self.play(Write(formula_text))
        self.wait()

        # Create formula as text to avoid LaTeX issues
        formula = Tex(
            r"x = $\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$",
            font_size=50
        )
        formula.next_to(formula_text, DOWN, buff=0.5)
        self.play(Write(formula))
        self.wait(2)

        # Discriminant label
        discriminant_label = Text("Discriminant: b² - 4ac", font_size=28, color=BLUE)
        discriminant_label.next_to(formula, DOWN, buff=0.5)

        self.play(Write(discriminant_label))
        self.wait(2)

        # Clear and show example
        self.play(
            FadeOut(formula_text),
            FadeOut(formula),
            FadeOut(discriminant_label)
        )

        # Example problem
        example_title = Text("Example: Solve x² - 5x + 6 = 0", font_size=36)
        example_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(example_title))
        self.wait()

        # Identify coefficients
        coeffs = VGroup(
            Text("a = 1", font_size=36),
            Text("b = -5", font_size=36),
            Text("c = 6", font_size=36)
        ).arrange(RIGHT, buff=0.8)
        coeffs.next_to(example_title, DOWN, buff=0.5)
        self.play(Write(coeffs))
        self.wait()

        # Apply formula
        solution = Tex(
            r"x = $\frac{-(-5) \pm \sqrt{(-5)^2 - 4(1)(6)}}{2(1)}$",
            font_size=36
        )
        solution.next_to(coeffs, DOWN, buff=0.5)
        self.play(Write(solution))
        self.wait()

        # Simplify
        simplified = Tex(
            r"x = $\frac{5 \pm \sqrt{25 - 24}}{2}$",
            font_size=36
        )
        simplified.next_to(solution, DOWN, buff=0.3)
        self.play(Write(simplified))
        self.wait()

        final = Tex(
            r"x = $\frac{5 \pm 1}{2}$",
            font_size=36
        )
        final.next_to(simplified, DOWN, buff=0.3)
        self.play(Write(final))
        self.wait()

        # Solutions
        solutions = VGroup(
            Text("x = 3", font_size=40, color=GREEN),
            Text("or", font_size=32),
            Text("x = 2", font_size=40, color=GREEN)
        ).arrange(RIGHT, buff=0.3)
        solutions.next_to(final, DOWN, buff=0.5)
        self.play(Write(solutions))
        self.wait(2)

        # Clear for graph
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob != title]
        )

        # Graph the parabola
        ax = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 8, 1],
            x_length=8,
            y_length=6,
            axis_config={"include_numbers": True}
        )
        ax.next_to(title, DOWN, buff=0.3)

        # The parabola
        parabola = ax.plot(
            lambda x: x**2 - 5*x + 6,
            color=BLUE,
            x_range=[-0.5, 5.5]
        )

        # Mark the solutions
        dot1 = Dot(ax.c2p(2, 0), color=RED, radius=0.1)
        dot2 = Dot(ax.c2p(3, 0), color=RED, radius=0.1)
        label1 = Text("x = 2", font_size=32).next_to(dot1, DOWN)
        label2 = Text("x = 3", font_size=32).next_to(dot2, DOWN)

        graph_label = Text("y = x² - 5x + 6", font_size=36)
        graph_label.next_to(ax, DOWN, buff=0.3)

        self.play(Create(ax))
        self.play(Create(parabola), Write(graph_label))
        self.wait()
        self.play(
            Create(dot1),
            Create(dot2),
            Write(label1),
            Write(label2)
        )
        self.wait(3)

        # Final message
        conclusion = Text(
            "These are the x-intercepts (roots) of the parabola!",
            font_size=32,
            color=YELLOW
        )
        conclusion.to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(3)
