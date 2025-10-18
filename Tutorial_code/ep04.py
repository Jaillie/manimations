from pickle import TRUE
from manim import *


class AllUpdaterTypes(Scene):
    def construct(self):
        red_dot = Dot(color=RED).shift(LEFT)
        pointer = Arrow(ORIGIN, RIGHT).next_to(red_dot, LEFT)
        pointer.add_updater(  #Place arrow left of dot
            lambda mob: mob.next_to(red_dot, LEFT)
        )

        def shifter(mob, dt):   # make dot move 2 munits Right/sec
            mob.shift(2*dt*RIGHT)
        red_dot.add_updater(shifter)

        def scene_scaler(dt): # scale mobjects depending on distance to ORIGIN
            for mob in self.mobjects:
                mob.set(width=2/(1 + np.linalg.norm(mob.get_center())))
        self.add_updater(scene_scaler)

        self.add(red_dot, pointer)
        self.update_self(0)
        self.wait(5)


class UpdaterAndAnimation(Scene):
    def construct(self):
        red_dot = Dot(color=RED).shift(LEFT)
        rotating_square = Square()
        rotating_square.add_updater(
            lambda mob, dt: mob.rotate(PI*dt)

        )

        def shifter(mob, dt):
            mob.shift(2*dt*RIGHT)
        red_dot.add_updater(shifter)

        self.add(red_dot, rotating_square)
        self.wait(1)
        red_dot.suspend_updating()
        self.wait(1)

        self.play(
            red_dot.animate.shift(UP),
            rotating_square.animate.move_to([-2, -2, 0])
        )
        self.wait(1)


class VectorUpdaterLine(Scene):
    def construct(self):
        line = NumberLine(x_range=[-5, 5])
        position = ValueTracker(0)  # assign initial value of tracker
        pointer = Vector(DOWN)
        pointer.add_updater(    # stick pointer to tracked position
            lambda mob: mob.next_to(
                line.number_to_point(position.get_value()), UP
            )
        )
        pointer.update()    # manual execution of update function
        self.add(line, pointer)
        self.wait()
        self.play(position.animate.set_value(4))    # change tracker value
        self.play(position.animate.set_value(-2))   # ... and to -2



class ValueTrackerPlot(Scene):
    def construct(self):
        a = ValueTracker(1)
        ax = Axes(x_range = [-2, 2, 1], y_range = [-8.5, 8.5, 1], x_length=4, y_length=6)
        parabola = ax.plot(lambda x: x**2, color=RED)
        parabola.add_updater(
            lambda mob: mob.become(ax.plot(lambda x: a.get_value() * x**2, color=RED))
        )
        a_number = DecimalNumber(
            a.get_value(),
            color=RED,
            num_decimal_places=3,
            show_ellipsis=True
        )
        a_number.add_updater(
            lambda mob: mob.set_value(a.get_value()).next_to(parabola, RIGHT)
        )
        self.add(ax, parabola, a_number)
        self.play(a.animate.set_value(2))
        self.play(a.animate.set_value(-2))
        self.play(a.animate.set_value(1))
