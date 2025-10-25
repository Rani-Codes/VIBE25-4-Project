from manim import *

class TreesAndNodes(Scene):
    def construct(self):
        # Set a dark background color, characteristic of 3Blue1Brown style
        self.camera.background_color = "#282828"

        # --- Scene 1: Introduction to Nodes and Edges ---
        # Display the initial title for the scene
        intro_title = Text("Understanding Trees: Nodes and Edges", font_size=48).to_edge(UP)
        self.play(Write(intro_title))
        self.wait(0.5)

        # Define and animate the concept of a "Node"
        node_def_text = Text("A Node (or Vertex)", font_size=36, color=BLUE_B).shift(UP*1.5 + LEFT*3)
        node_circle = Dot(radius=0.3, color=BLUE_C).next_to(node_def_text, DOWN, buff=0.5)
        node_label = MathTex(r"\text{Node}", font_size=30, color=BLUE_C).next_to(node_circle, RIGHT, buff=0.2)
        node_group = VGroup(node_circle, node_label)

        self.play(
            FadeIn(node_def_text, shift=UP),
            Create(node_circle)
        )
        self.play(Write(node_label))
        self.wait(1)

        # Define and animate the concept of an "Edge"
        edge_def_text = Text("An Edge (or Link)", font_size=36, color=YELLOW_B).shift(UP*1.5 + RIGHT*3)
        node_circle_2 = Dot(radius=0.3, color=BLUE_C).next_to(edge_def_text, DOWN, buff=0.5).shift(LEFT*1)
        node_circle_3 = Dot(radius=0.3, color=BLUE_C).next_to(edge_def_text, DOWN, buff=0.5).shift(RIGHT*1)
        edge_line = Line(node_circle_2.get_center(), node_circle_3.get_center(), color=YELLOW_C)
        edge_label = MathTex(r"\text{Edge}", font_size=30, color=YELLOW_C).next_to(edge_line, UP, buff=0.2)
        edge_group = VGroup(node_circle_2, node_circle_3, edge_line, edge_label)

        self.play(
            FadeIn(edge_def_text, shift=UP),
            Create(node_circle_2), Create(node_circle_3),
            Create(edge_line)
        )
        self.play(Write(edge_label))
        self.wait(1)

        # Fade out the node/edge definitions, keeping the main title for transformation
        self.play(FadeOut(node_def_text, node_group, edge_def_text, edge_group))
        self.wait(0.5)

        # --- Scene 2: Building a Tree ---
        # Transform the title to introduce the tree structure
        tree_title = Text("Building a Tree Structure", font_size=48).to_edge(UP)
        self.play(Transform(intro_title, tree_title))

        # Define positions for all nodes in the tree
        node_pos = {
            "root": np.array([0, 2.5, 0]),
            "L1_1": np.array([-2, 0.5, 0]),
            "L1_2": np.array([2, 0.5, 0]),
            "L2_1": np.array([-3, -1.5, 0]),
            "L2_2": np.array([-1, -1.5, 0]),
            "L2_3": np.array([1, -1.5, 0]),
            "L2_4": np.array([3, -1.5, 0]),
        }

        # Create Dot objects for each node
        nodes = {}
        for key, pos in node_pos.items():
            nodes[key] = Dot(point=pos, radius=0.25, color=BLUE_C)

        # VGroup to hold all edges and nodes for easier manipulation
        edges = VGroup()
        all_nodes_mobjects = VGroup()

        # Animate the creation of the root node
        self.play(FadeIn(nodes["root"]))
        all_nodes_mobjects.add(nodes["root"])
        self.wait(0.5)

        # Animate the creation of Level 1 nodes and their edges
        self.play(FadeIn(nodes["L1_1"], nodes["L1_2"]))
        edge1 = Line(nodes["root"].get_center(), nodes["L1_1"].get_center(), color=GREY_B)
        edge2 = Line(nodes["root"].get_center(), nodes["L1_2"].get_center(), color=GREY_B)
        self.play(Create(edge1), Create(edge2))
        edges.add(edge1, edge2)
        all_nodes_mobjects.add(nodes["L1_1"], nodes["L1_2"])
        self.wait(0.5)

        # Animate the creation of Level 2 nodes and their edges
        self.play(FadeIn(nodes["L2_1"], nodes["L2_2"], nodes["L2_3"], nodes["L2_4"]))
        edge3 = Line(nodes["L1_1"].get_center(), nodes["L2_1"].get_center(), color=GREY_B)
        edge4 = Line(nodes["L1_1"].get_center(), nodes["L2_2"].get_center(), color=GREY_B)
        edge5 = Line(nodes["L1_2"].get_center(), nodes["L2_3"].get_center(), color=GREY_B)
        edge6 = Line(nodes["L1_2"].get_center(), nodes["L2_4"].get_center(), color=GREY_B)
        self.play(Create(edge3), Create(edge4), Create(edge5), Create(edge6))
        edges.add(edge3, edge4, edge5, edge6)
        all_nodes_mobjects.add(nodes["L2_1"], nodes["L2_2"], nodes["L2_3"], nodes["L2_4"])
        self.wait(1)

        # Group all tree components and add a definition of a tree
        tree_group = VGroup(all_nodes_mobjects, edges)
        tree_def = Text("A Tree: a connected graph with no cycles.", font_size=36, color=WHITE).next_to(tree_group, DOWN, buff=1)
        self.play(Write(tree_def))
        self.wait(2)

        self.play(FadeOut(tree_def))

        # --- Scene 3: Tree Terminology ---
        # Transform the title again for terminology section
        term_title = Text("Key Tree Terminology", font_size=48).to_edge(UP)
        self.play(Transform(intro_title, term_title))
        self.play(tree_group.animate.shift(UP*0.5)) # Shift tree up slightly to make room for labels

        # Highlight and label the Root Node
        root_label = Text("Root Node", font_size=36, color=RED_C).next_to(nodes["root"], UP, buff=0.3)
        self.play(nodes["root"].animate.set_color(RED_C), Write(root_label))
        self.wait(1.5)
        self.play(nodes["root"].animate.set_color(BLUE_C), FadeOut(root_label))

        # Highlight and label Parent and Child Nodes
        parent_label = Text("Parent", font_size=36, color=GREEN_C).next_to(nodes["L1_1"], LEFT, buff=0.3)
        child_label = Text("Child", font_size=36, color=GREEN_SCREEN).next_to(nodes["L2_1"], LEFT, buff=0.3) # Using GREEN_SCREEN for better contrast
        self.play(
            nodes["L1_1"].animate.set_color(GREEN_C), Write(parent_label),
            nodes["L2_1"].animate.set_color(GREEN_SCREEN), Write(child_label),
            Indicate(Line(nodes["L1_1"].get_center(), nodes["L2_1"].get_center()), color=GREEN_YELLOW)
        )
        self.wait(1.5)
        self.play(
            nodes["L1_1"].animate.set_color(BLUE_C), FadeOut(parent_label),
            nodes["L2_1"].animate.set_color(BLUE_C), FadeOut(child_label)
        )

        # Highlight and label Leaf Nodes
        leaf_nodes = VGroup(nodes["L2_1"], nodes["L2_2"], nodes["L2_3"], nodes["L2_4"])
        leaf_label = Text("Leaf Nodes (no children)", font_size=36, color=PURPLE_C).next_to(leaf_nodes, DOWN, buff=0.5)
        self.play(leaf_nodes.animate.set_color(PURPLE_C), Write(leaf_label))
        self.wait(2)
        self.play(leaf_nodes.animate.set_color(BLUE_C), FadeOut(leaf_label))

        # Highlight and label a Path
        path_nodes = VGroup(nodes["root"], nodes["L1_1"], nodes["L2_1"])
        path_edges = VGroup(edge1, edge3)
        path_label = Text("A Path", font_size=36, color=ORANGE).next_to(path_nodes[1], LEFT, buff=0.5)
        self.play(
            path_nodes.animate.set_color(ORANGE),
            path_edges.animate.set_stroke(color=ORANGE, width=6),
            Write(path_label)
        )
        self.wait(2)
        self.play(
            path_nodes.animate.set_color(BLUE_C),
            path_edges.animate.set_stroke(color=GREY_B, width=DEFAULT_STROKE_WIDTH),
            FadeOut(path_label)
        )

        # Illustrate Depth/Level of the tree
        # Define horizontal lines for each level
        level_line_length = 8
        level_0_line = Line(LEFT * level_line_length/2, RIGHT * level_line_length/2, color=GREY_A).set_y(nodes["root"].get_y() - nodes["root"].radius - 0.2)
        level_1_line = Line(LEFT * level_line_length/2, RIGHT * level_line_length/2, color=GREY_A).set_y(nodes["L1_1"].get_y() - nodes["L1_1"].radius - 0.2)
        level_2_line = Line(LEFT * level_line_length/2, RIGHT * level_line_length/2, color=GREY_A).set_y(nodes["L2_1"].get_y() - nodes["L2_1"].radius - 0.2)

        # Position labels relative to the level lines
        level_0_label = Text("Level 0 (Depth 0)", font_size=28, color=WHITE).next_to(level_0_line, LEFT, buff=0.5)
        level_1_label = Text("Level 1 (Depth 1)", font_size=28, color=WHITE).next_to(level_1_line, LEFT, buff=0.5)
        level_2_label = Text("Level 2 (Depth 2)", font_size=28, color=WHITE).next_to(level_2_line, LEFT, buff=0.5)

        self.play(Write(level_0_label), Create(level_0_line))
        self.wait(0.5)
        self.play(Write(level_1_label), Create(level_1_line))
        self.wait(0.5)
        self.play(Write(level_2_label), Create(level_2_line))
        self.wait(2)
        self.play(FadeOut(level_0_label, level_1_label, level_2_label, level_0_line, level_1_line, level_2_line))

        # Highlight and label a Subtree
        subtree_nodes = VGroup(nodes["L1_1"], nodes["L2_1"], nodes["L2_2"])
        subtree_edges = VGroup(edge3, edge4)
        subtree_group = VGroup(subtree_nodes, subtree_edges)
        subtree_box = SurroundingRectangle(subtree_group, color=TEAL_C, buff=0.2)
        subtree_label = Text("A Subtree", font_size=36, color=TEAL_C).next_to(subtree_box, UP, buff=0.3)

        self.play(Create(subtree_box), Write(subtree_label))
        self.wait(2)
        self.play(FadeOut(subtree_box, subtree_label))

        # Fade out the entire tree and the title
        self.play(FadeOut(tree_group, intro_title))
        self.wait(1)

        # --- Scene 4: Conclusion and Examples ---
        # Display a summary and real-world examples of trees
        summary_text = Text("Trees are fundamental structures in Computer Science and Math.", font_size=40, color=WHITE).to_edge(UP)
        examples_text = Text("Examples: File systems, Family trees, Decision trees.", font_size=36, color=GREY_A).next_to(summary_text, DOWN, buff=1)
        self.play(Write(summary_text))
        self.play(FadeIn(examples_text, shift=DOWN))
        self.wait(3)
        self.play(FadeOut(summary_text, examples_text))