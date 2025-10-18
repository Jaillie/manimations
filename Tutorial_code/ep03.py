from turtle import left
from manim import *

from manim import ManimColor


class BasicAnimations(Scene):
    def construct(self):
        polys = VGroup(
            *[RegularPolygon(5, radius=1, fill_opacity=0.5, 
            color = ManimColor.from_hsv((j/5, 1., 1.)))
             for j in range(5)
             ]
        ).arrange(RIGHT)
        self.play(DrawBorderThenFill(polys), run_time=2)
        self.play(
            Rotate(polys[0], PI, rate_func=lambda t: t),
            Rotate(polys[1], PI, rate_func=smooth),
            Rotate(polys[2], PI, rate_func=lambda t: np.sin(t*PI)),
            Rotate(polys[3], PI, rate_func=there_and_back),
            Rotate(polys[4], PI, rate_func=lambda t: 1 - abs(1-2*t)),
            run_time=2
        )
        self.wait()


class LaggingGroup(Scene):
    def construct(self):
        squares = VGroup(
            *[Square(color = ManimColor.from_hsv((j/20, 1., 1.)), fill_opacity = 0.5) for j in range (20)]).arrange_in_grid(4,5).scale(0.75)
        self.play(AnimationGroup(*[FadeIn(s) for s in squares], lag_ratio=0.15))

class AnimateSyntax(Scene):
    def construct(self):
        s = Square(color=GREEN, fill_opacity =0.5)
        c = Circle(color=RED, fill_opacity=0.5)
        self.add(s, c)
        self.play(s.animate.shift(UP), c.animate.shift(DOWN))
        self.play(VGroup(s, c).animate.arrange(RIGHT, buff=1))
        self.play(c.animate(rate_func=linear).shift(RIGHT).scale(2))

class AnimateProblem(Scene):
    def construct(self):
        left_square = Square()
        right_square = Square()
        VGroup(left_square, right_square).arrange(RIGHT, buff=1)
        self.play(left_square.animate.rotate(PI), Rotate(right_square, PI), run_time=2)
        self.wait()


class AnimationMechanisms(Scene):
    def construct(self):
        c = Circle()

        c.generate_target()
        c.target.set_fill(color=GREEN, opacity=0.5)
        c.target.shift(2*RIGHT + UP).scale(0.5)

        self.add(c)
        self.wait()
        self.play(MoveToTarget(c))

        s = Square()
        s.save_state()
        self.play(FadeIn(s))
        self.play(s.animate.set_color(PURPLE).set_opacity(0.5).shift(2*LEFT).scale(3))
        self.play(s.animate.shift(5*DOWN).rotate(PI/4))
        self.wait()
        self.play(Restore(s), run_time=2)
        self.wait()


class SimpleCustomAnimation(Scene):
    def construct(self):
        def spiral_out(mobject, t):
            radius = 4*t
            angle = 2*t * 2*PI
            mobject.move_to(radius*(np.cos(angle)*RIGHT + np.sin(angle)*UP))
            mobject.set_color(ManimColor.from_hsv((t, 1., 0.5)))
            mobject.set_opacity(1-t)

        d = Dot(color=WHITE)
        self.add(d)
        self.play(UpdateFromAlphaFunc(d, spiral_out, run_time=3))





class Disperse(Animation):
    def __init__(self, mobject, dot_radius=0.05, dot_number=100, **kwargs):
        super().__init__(mobject, **kwargs)
        self.dot_radius = dot_radius
        self.dot_number = dot_number
    
    def begin(self):
        dots = VGroup(
            *[Dot(radius=self.dot_radius, color=BLUE).move_to(self.mobject.point_from_proportion(p))
              for p in np.linspace(0, 1, self.dot_number)]
        )
        for dot in dots:
            dot.initial_position = dot.get_center()
            dot.shift_vector = 2*(dot.get_center() - self.mobject.get_center())
        dots.set_opacity(0)
        self.mobject.add(dots)
        self.dots = dots
        super().begin()
        
    def clean_up_from_scene(self, scene):
        super().clean_up_from_scene(scene)
        scene.remove(self.dots)

    def interpolate_mobject(self, alpha):
        alpha = self.rate_func(alpha)  # manually apply rate function
        if alpha <= 0.5:
            self.mobject.set_opacity(1 - 2*alpha, family=False)
            self.dots.set_opacity(2*alpha)
        else:
            self.mobject.set_opacity(0)
            self.dots.set_opacity(2*(1 - alpha))
            for dot in self.dots:
                dot.move_to(dot.initial_position + 2*(alpha-0.5)*dot.shift_vector)
            
            

class CustomAnimationExample(Scene):
    def construct(self):
        st = Star(color=YELLOW, fill_opacity=1).scale(3)
        self.add(st)
        self.wait()
        self.play(Disperse(st, dot_number=200, run_time=4))


