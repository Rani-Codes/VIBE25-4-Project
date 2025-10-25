from manim import *

class SimpleAddition(Scene):
    def construct(self):
        # 1. Introduction: Introduce the concept of addition.
        intro_text = Text("Let's explore addition!", font_size=72)
        self.play(Write(intro_text))
        self.wait(1)
        self.play(FadeOut(intro_text))

        # 2. Present the first addition problem (2 + 3).
        problem_tex_1 = MathTex("2", "+", "3", "=", "?").to_edge(UP)
        self.play(Write(problem_tex_1))
        self.wait(0.5)

        # 3. Visualize the first number (2) with blue dots.
        dots_two = VGroup(*[Dot(radius=0.2, color=BLUE) for _ in range(2)])
        dots_two.arrange(RIGHT, buff=0.3)
        dots_two.next_to(problem_tex_1[0], DOWN, buff=1.0)
        self.play(Create(dots_two))
        self.wait(0.5)

        # 4. Visualize the second number (3) with yellow dots, and show the plus sign.
        dots_three = VGroup(*[Dot(radius=0.2, color=YELLOW) for _ in range(3)])
        dots_three.arrange(RIGHT, buff=0.3)
        dots_three.next_to(problem_tex_1[2], DOWN, buff=1.0)

        plus_sign_visual_1 = MathTex("+").scale(1.5)
        plus_sign_visual_1.move_to(
            (dots_two.get_right() + dots_three.get_left()) / 2
        )
        self.play(Create(dots_three), Write(plus_sign_visual_1))
        self.wait(1)

        # 5. Combine the dots: Animate the dots moving together to form a single group.
        # Create a target VGroup for all dots combined, arranged at the center.
        combined_dots_target_1 = VGroup(*[Dot(radius=0.2, color=BLUE) for _ in range(2)],
                                        *[Dot(radius=0.2, color=YELLOW) for _ in range(3)])
        combined_dots_target_1.arrange(RIGHT, buff=0.3).move_to(ORIGIN)

        # Transform the individual dot groups into their positions within the combined group.
        self.play(
            Transform(dots_two, combined_dots_target_1[:2]),
            Transform(dots_three, combined_dots_target_1[2:]),
            FadeOut(plus_sign_visual_1),
            run_time=1.5
        )
        self.wait(0.5)

        # Create a new VGroup from the transformed dots for easier counting.
        all_combined_dots_1 = VGroup(*dots_two, *dots_three)

        # 6. Count the combined dots one by one and update a counter.
        count_label_1 = Text("Count: 0", font_size=40).next_to(all_combined_dots_1, DOWN, buff=0.7)
        self.play(Write(count_label_1))

        for i, dot in enumerate(all_combined_dots_1):
            original_color = dot.get_color() # Store original color to revert later
            self.play(
                dot.animate.set_color(GREEN).scale(1.2), # Highlight dot in green and enlarge
                count_label_1.animate.become(Text(f"Count: {i+1}", font_size=40).next_to(all_combined_dots_1, DOWN, buff=0.7)),
                run_time=0.5
            )
            self.play(dot.animate.set_color(original_color).scale(1/1.2), run_time=0.3) # Revert dot to original state
        self.wait(0.5)

        # 7. Reveal the answer (5) by updating the equation and fading out the dots.
        self.play(
            FadeOut(all_combined_dots_1, shift=DOWN), # Fade out the dots
            FadeOut(count_label_1),
            TransformMatchingTex(problem_tex_1, MathTex("2", "+", "3", "=", "5").to_edge(UP)) # Update equation to show result
        )
        self.wait(1.5)

        # 8. Second Example: Repeat the process for 4 + 1 to reinforce the concept.
        self.play(FadeOut(problem_tex_1)) # Clear the first problem
        self.wait(0.5)

        problem_tex_2 = MathTex("4", "+", "1", "=", "?").to_edge(UP)
        self.play(Write(problem_tex_2))

        dots_four = VGroup(*[Dot(radius=0.2, color=ORANGE) for _ in range(4)])
        dots_four.arrange(RIGHT, buff=0.3).next_to(problem_tex_2[0], DOWN, buff=1.0)

        dots_one = VGroup(*[Dot(radius=0.2, color=PURPLE) for _ in range(1)])
        dots_one.arrange(RIGHT, buff=0.3).next_to(problem_tex_2[2], DOWN, buff=1.0)

        plus_sign_visual_2 = MathTex("+").scale(1.5)
        plus_sign_visual_2.move_to(
            (dots_four.get_right() + dots_one.get_left()) / 2
        )

        self.play(Create(dots_four), Create(dots_one), Write(plus_sign_visual_2))
        self.wait(1)

        combined_dots_target_2 = VGroup(*[Dot(radius=0.2, color=ORANGE) for _ in range(4)],
                                        *[Dot(radius=0.2, color=PURPLE) for _ in range(1)])
        combined_dots_target_2.arrange(RIGHT, buff=0.3).move_to(ORIGIN)

        self.play(
            Transform(dots_four, combined_dots_target_2[:4]),
            Transform(dots_one, combined_dots_target_2[4:]),
            FadeOut(plus_sign_visual_2),
            run_time=1.5
        )
        self.wait(0.5)

        all_combined_dots_2 = VGroup(*dots_four, *dots_one)

        count_label_2 = Text("Count: 0", font_size=40).next_to(all_combined_dots_2, DOWN, buff=0.7)
        self.play(Write(count_label_2))

        for i, dot in enumerate(all_combined_dots_2):
            original_color = dot.get_color()
            self.play(
                dot.animate.set_color(GREEN).scale(1.2),
                count_label_2.animate.become(Text(f"Count: {i+1}", font_size=40).next_to(all_combined_dots_2, DOWN, buff=0.7)),
                run_time=0.4
            )
            self.play(dot.animate.set_color(original_color).scale(1/1.2), run_time=0.2)
        self.wait(0.5)

        # Reveal the answer (5) for the second problem.
        self.play(
            FadeOut(all_combined_dots_2, shift=DOWN),
            FadeOut(count_label_2),
            TransformMatchingTex(problem_tex_2, MathTex("4", "+", "1", "=", "5").to_edge(UP))
        )
        self.wait(2)

        # 9. Final fade out of all elements.
        self.play(FadeOut(self.mobjects))