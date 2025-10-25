from manim import *

class BinarySearchVisualization(Scene):
    def construct(self):
        # 1. Setup Data and Target
        # The sorted array of numbers to search through
        data = [5, 12, 18, 24, 30, 37, 42, 55, 60, 71]
        # The value we are searching for
        target_value = 42 # Change this to test 'not found' case, e.g., 20

        # Create array elements as VGroup of Square and MathTex
        # Each element is a square with its number inside
        array_elements = VGroup()
        for i, num in enumerate(data):
            square = Square(side_length=1.0, color=BLUE_GREY, fill_opacity=0.2)
            number_text = MathTex(str(num)).move_to(square.center)
            element = VGroup(square, number_text)
            array_elements.add(element)

        # Arrange the array elements horizontally and shift them up
        array_elements.arrange(RIGHT, buff=0.1).shift(UP * 0.5)
        # Animate the creation of array elements with a slight delay for each
        self.play(LaggedStart(*[Create(element) for element in array_elements], lag_ratio=0.1), run_time=2)
        self.wait(0.5)

        # Add index labels below the array elements
        index_labels = VGroup()
        for i in range(len(data)):
            index_label = MathTex(str(i), font_size=30).next_to(array_elements[i], DOWN, buff=0.2)
            index_labels.add(index_label)
        # Animate the writing of index labels
        self.play(LaggedStart(*[Write(label) for label in index_labels], lag_ratio=0.05), run_time=1.5)
        self.wait(0.5)

        # Display the target value at the top-left
        target_display = VGroup(
            Text("Target = ", font_size=40),
            MathTex(str(target_value), font_size=40, color=ORANGE)
        ).arrange(RIGHT, buff=0.2).to_edge(UL).shift(RIGHT*0.5)
        self.play(Write(target_display))
        self.wait(1)

        # 2. Initialize Pointers and their labels/text displays
        low_idx = 0
        high_idx = len(data) - 1

        # Low pointer (blue triangle) and its label
        low_pointer = Triangle(color=BLUE, fill_opacity=1).scale(0.2).next_to(array_elements[low_idx], UP, buff=0.5)
        low_label = Text("low", font_size=25, color=BLUE).next_to(low_pointer, UP, buff=0.1)
        # Text display for the 'low' index value
        low_idx_text = MathTex(f"\\texttt{{low}}: {low_idx}", font_size=30, color=BLUE).next_to(target_display, DOWN, buff=0.5).align_to(target_display, LEFT)

        # High pointer (yellow triangle) and its label
        high_pointer = Triangle(color=YELLOW, fill_opacity=1).scale(0.2).next_to(array_elements[high_idx], UP, buff=0.5)
        high_label = Text("high", font_size=25, color=YELLOW).next_to(high_pointer, UP, buff=0.1)
        # Text display for the 'high' index value
        high_idx_text = MathTex(f"\\texttt{{high}}: {high_idx}", font_size=30, color=YELLOW).next_to(low_idx_text, DOWN, buff=0.2).align_to(low_idx_text, LEFT)

        # Mid pointer (green triangle) and its label
        # It's initialized to the first calculated mid_idx
        initial_mid_idx = (low_idx + high_idx) // 2
        mid_pointer = Triangle(color=GREEN, fill_opacity=1).scale(0.2).next_to(array_elements[initial_mid_idx], UP, buff=0.5)
        mid_label = Text("mid", font_size=25, color=GREEN).next_to(mid_pointer, UP, buff=0.1)
        # Text display for the 'mid' index value
        mid_idx_text = MathTex(f"\\texttt{{mid}}: {initial_mid_idx}", font_size=30, color=GREEN).next_to(high_idx_text, DOWN, buff=0.2).align_to(high_idx_text, LEFT)

        # Animate the fading in of all pointers and their index texts
        self.play(
            FadeIn(low_pointer, low_label, low_idx_text),
            FadeIn(high_pointer, high_label, high_idx_text),
            FadeIn(mid_pointer, mid_label, mid_idx_text)
        )
        self.wait(1)

        # Status text to display algorithm steps at the bottom
        status_text = Text("Starting binary search...", font_size=35).to_edge(DOWN)
        self.play(Write(status_text))
        self.wait(1)

        # 3. Binary Search Loop
        found = False
        while low_idx <= high_idx:
            # Calculate the new mid index for the current search range
            new_mid_idx = (low_idx + high_idx) // 2

            # Animate mid pointer and text updates
            # The mid pointer moves to the new mid_idx, and its label follows
            # The mid_idx_text is transformed to show the new index
            self.play(
                mid_pointer.animate.next_to(array_elements[new_mid_idx], UP, buff=0.5),
                mid_label.animate.next_to(mid_pointer, UP, buff=0.1),
                Transform(mid_idx_text, MathTex(f"\\texttt{{mid}}: {new_mid_idx}", font_size=30, color=GREEN).align_to(high_idx_text, LEFT))
            )
            # Update the internal mid_idx variable
            mid_idx = new_mid_idx

            current_element_value = data[mid_idx]

            # Highlight the square of the current mid element in green
            self.play(array_elements[mid_idx][0].animate.set_color(GREEN), run_time=0.7)
            self.wait(0.5)

            # Compare target with mid element
            if current_element_value == target_value:
                # Target found! Update status text and highlight the found element
                self.play(status_text.animate.set_value(f"Found {target_value} at index {mid_idx}!").set_color(ORANGE))
                self.play(
                    array_elements[mid_idx][0].animate.set_color(ORANGE), # Square to orange
                    array_elements[mid_idx][1].animate.set_color(BLACK)   # Number text to black for contrast
                )
                found = True
                break # Exit the loop
            elif current_element_value < target_value:
                # Target is greater than mid element, search in the right half
                self.play(status_text.animate.set_value(f"{current_element_value} < {target_value}. Search right half.").set_color(BLUE))
                # Animate fading out the left half (from low to mid, inclusive) by changing their color to grey
                animations = []
                for i in range(low_idx, mid_idx + 1):
                    animations.append(array_elements[i][0].animate.set_color(GREY_D).set_fill(GREY_D, opacity=0.1))
                    animations.append(array_elements[i][1].animate.set_color(GREY_D))
                    animations.append(index_labels[i].animate.set_color(GREY_D))
                self.play(*animations, run_time=1)
                
                low_idx = mid_idx + 1 # Update low index to mid_idx + 1
                # Animate low pointer and text updates
                self.play(
                    low_pointer.animate.next_to(array_elements[low_idx], UP, buff=0.5),
                    low_label.animate.next_to(low_pointer, UP, buff=0.1),
                    Transform(low_idx_text, MathTex(f"\\texttt{{low}}: {low_idx}", font_size=30, color=BLUE).align_to(target_display, LEFT))
                )
            else: # current_element_value > target_value
                # Target is less than mid element, search in the left half
                self.play(status_text.animate.set_value(f"{current_element_value} > {target_value}. Search left half.").set_color(YELLOW))
                # Animate fading out the right half (from mid to high, inclusive)
                animations = []
                for i in range(mid_idx, high_idx + 1):
                    animations.append(array_elements[i][0].animate.set_color(GREY_D).set_fill(GREY_D, opacity=0.1))
                    animations.append(array_elements[i][1].animate.set_color(GREY_D))
                    animations.append(index_labels[i].animate.set_color(GREY_D))
                self.play(*animations, run_time=1)

                high_idx = mid_idx - 1 # Update high index to mid_idx - 1
                # Animate high pointer and text updates
                self.play(
                    high_pointer.animate.next_to(array_elements[high_idx], UP, buff=0.5),
                    high_label.animate.next_to(high_pointer, UP, buff=0.1),
                    Transform(high_idx_text, MathTex(f"\\texttt{{high}}: {high_idx}", font_size=30, color=YELLOW).align_to(low_idx_text, LEFT))
                )
            
            self.wait(1.5) # Pause after each step

        # Final state after the loop
        if not found:
            # If target was not found, update status and fade out all pointers/texts
            self.play(status_text.animate.set_value(f"Target {target_value} not found in array.").set_color(RED))
            self.play(FadeOut(low_pointer, low_label, high_pointer, high_label, mid_pointer, mid_label, low_idx_text, high_idx_text, mid_idx_text))
        else:
            # If target was found, fade out all pointers and texts except the found element
            self.play(FadeOut(low_pointer, low_label, high_pointer, high_label, mid_pointer, mid_label, low_idx_text, high_idx_text, mid_idx_text))

        self.wait(3) # Final pause