from manim import *

class NestedCirclesToYoink(Scene):
    def construct(self):
        # Create multiple nested circles
        outer_circle = Circle(color=BLUE, fill_opacity=0.3).scale(2)
        middle_circle = Circle(color=GREEN, fill_opacity=0.3).scale(1.5)
        inner_circle = Circle(color=RED, fill_opacity=0.3).scale(1)

        # Group all circles together
        nested_circles = VGroup(outer_circle, middle_circle, inner_circle)

        # Create the text "yoink"
        yoink_text = Text("yoink", font_size=96, color=YELLOW)

        # Animation: Draw the nested circles
        self.play(Create(outer_circle), Create(middle_circle), Create(inner_circle))
        self.wait(1)

        # Animation: Transform all circles into the text "yoink"
        self.play(Transform(nested_circles, yoink_text))
        self.wait(2)
