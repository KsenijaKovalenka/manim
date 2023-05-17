from manim import *
from manim.mobject.geometry.tips import StealthTip

FONT_SIZE = 63

physics_template = TexTemplate()
physics_template.add_to_preamble(r"\usepackage{physics}")

imbedding_u = -2.91
imbedding_d = -1.32
weight_u = 6.07
weight_d = 4.39

class PTex(MathTex):
    def __init__(self, *args, font_size=FONT_SIZE, **kwargs):
        super().__init__(
            *args,
            font_size=font_size,
            tex_template=physics_template,
            **kwargs
        )

def get_unit_vector(vec):
  return vec / np.linalg.norm(vec)

class Qbit(VGroup):
  def __init__(self,
               radius=2,
               axis_scale=1.3,
               axis_colors=BLUE,
               labels_color=WHITE,
               buff_labels=0.1,
               **kwargs):
    super().__init__(**kwargs)
    axes = VGroup(*[
      Arrow(
        ORIGIN,
        get_unit_vector(DIRECTION) * radius * axis_scale,
        buff=0,
        color=axis_colors,
        # tip_shape=StealthTip
      )
      for DIRECTION in [
        UP, RIGHT, DOWN+LEFT
      ]
    ])
    labels = VGroup(*[
      MathTex(f"{s}")
        .next_to(a, get_unit_vector(a.get_end()), buff=buff_labels)
        .set_color(labels_color)
      for s,a in zip("zyx", axes)
    ])
    circle = Circle(radius=radius)

    self.add(axes, circle, labels)
    self.axes = axes
    self.circle = circle
    self.labels = labels

  def get_arrow(self, direction, tip_shape=StealthTip, **kwargs):
    center = self.circle.get_center()
    return Arrow(
        center,
        center + get_unit_vector(direction) * self.circle.width/2,
        buff=0,
        tip_shape=tip_shape,
        **kwargs
      )


class Gate3(VGroup):
  def __init__(self, radius=0.8, arrow_scale=1.8, fill_opacity=1, fill_color=BLACK, **kwargs):
    super().__init__()
    arc = Arc(radius, 0, PI)
    down_line = Line(LEFT*radius, RIGHT*radius).next_to(arc, DOWN, buff=0)
    arc_path = VMobject(fill_opacity=fill_opacity, fill_color=fill_color, **kwargs)
    arc_path.set_points([
      *arc.get_all_points(),
      *down_line.get_all_points(),
    ])
    arrow = Arrow(
      arc_path.get_corner(DL), 
      arc_path.get_corner(UR)
    ).scale(arrow_scale)
    self.add(arc_path, arrow)


def extract_all_submobs(grp, mob: Mobject):
  if len(mob.submobjects) == 0:
    grp.append(mob)
  else:
    for submob in mob.submobjects:
      extract_all_submobs(grp, submob)

def get_intersection_updater_sub_recursive(pre_mob, bk):
  grp = []
  extract_all_submobs(grp, pre_mob)
  def updater(pos_mob):
    pos_mob.become(
      VGroup(*[
          Intersection(submob, bk).match_style(submob)
          for submob in grp
      ])
    )
  return updater

class MaskAnimationScene(Scene):
    def construct(self):
        t1 = VGroup(
            VGroup(Circle(), Triangle()).arrange(RIGHT),
            Square()
        ).arrange(DOWN)

        t2 = Text("HELLO").to_edge(DOWN)
        bk_helper = Square(color=BLUE)\
            .scale(5).set_opacity(0.2)
        self.add(bk_helper)
        self.play(
          self.mask_anim(t1, bk_helper),
          self.mask_anim(t2, bk_helper),
        )
        self.wait()

    def mask_anim(self,
                  pre_mob,
                  background_helper,
                  mask_func = lambda mob,alpha: mob.shift(LEFT*alpha*5),
                  **kwargs):
        pre_mob.save_state()
        pre_mob_u = VMobject()
        def pre_mob_updater(mob, alpha):
          pre_mob.restore()
          mask_func(pre_mob, alpha)
          get_intersection_updater_sub_recursive(pre_mob, background_helper)(mob)

        pre_mob_updater(pre_mob_u, 0)
        self.remove(pre_mob)
        self.add(pre_mob_u)
        return UpdateFromAlphaFunc(pre_mob_u, pre_mob_updater, remover=True, **kwargs)


class MainScene(MaskAnimationScene):
  def show_gate(self, mob, slider, rate_func=linear, **kwargs):
    mob.next_to(slider, RIGHT, buff=0.1)
    return mob.animate(rate_func=rate_func, **kwargs).move_to(slider.get_center())

  def construct(self):
    """
    Mobject definitions
    """
    u_qbit = Qbit().scale(0.7).to_corner(UL).to_edge(UP, buff=0.1)
    d_qbit = Qbit().scale(0.7).to_corner(DL).to_edge(DOWN, buff=0.1)

    u_arrow = u_qbit.get_arrow(UP, color=PURPLE) 
    d_arrow = d_qbit.get_arrow(UP, color=PURPLE) 

    u_slider = Line(LEFT*2, RIGHT*2)
    d_slider = u_slider.copy()

    u_slider.match_y(u_qbit.circle).to_edge(RIGHT,buff=0)
    d_slider.match_y(d_qbit.circle).to_edge(RIGHT,buff=0)

    _G1 = PTex(r"\ket{q_1}").next_to(u_qbit, RIGHT, buff=1).match_y(u_slider)
    _G2 = PTex(r"\ket{q_2}").match_y(d_slider).align_to(_G1, LEFT)

    u_EQUAL = PTex("=").next_to(_G1, RIGHT, buff=0.3)
    d_EQUAL = PTex("=").next_to(_G2, RIGHT, buff=0.3)

    u_formula_1 = Matrix([[1],[0]]).next_to(u_EQUAL, RIGHT, buff=0.3)
    d_formula_1 = Matrix([[1],[0]]).next_to(d_EQUAL, RIGHT, buff=0.3)

    u_formula_11 = VGroup(
      # MathTex(r"\frac{1}{\sqrt{2}}"),
      Matrix([[0.12],["0.99i"]])
    ).arrange(RIGHT, buff=0.1).next_to(u_EQUAL, RIGHT, buff=0.3)

    u_formula_2 = VGroup(
      # MathTex(r"\frac{1}{\sqrt{2}}"),
      Matrix([[-0.01],["-i"]])
    ).arrange(RIGHT, buff=0.1).next_to(u_EQUAL, RIGHT, buff=0.3)

    d_formula_11 = VGroup(
      # MathTex(r"\frac{1}{\sqrt{2}}"),
      Matrix([[0.79],["0.61i"]])
    ).arrange(RIGHT, buff=0.1).next_to(d_EQUAL, RIGHT, buff=0.3)

    d_formula_2 = VGroup(
      # MathTex(r"\frac{1}{\sqrt{2}}"),
      Matrix([[-0.72],["-0.69i"]])
    ).arrange(RIGHT, buff=0.1).next_to(d_EQUAL, RIGHT, buff=0.3)

    u_formula_3 = VGroup(
      MathTex(r"-i"),
      Matrix([[0],[1]])
    ).arrange(RIGHT, buff=0.1).next_to(u_EQUAL, RIGHT, buff=0.3)

    phantom_bk = Rectangle(
      width=u_slider.get_length(),
      height=config.frame_height,
      fill_opacity=0,
      color=TEAL,
      stroke_opacity=0
    ).match_x(u_slider)

    """
    Gates creation
    """
    # GATE 1
    u_gate_1 =  VGroup(
      Rectangle(fill_opacity=1, fill_color=BLACK),
      PTex("R_x(-2.91)"),
    )
    u_gate_1[0].surround(u_gate_1[1], stretch=True)
    d_gate_1 =  VGroup(
      Rectangle(fill_opacity=1, fill_color=BLACK),
      PTex("R_x(-1.32)"),
    )
    d_gate_1[0].surround(d_gate_1[1], stretch=True)
    # GATE 1.1
    u_gate_11 =  VGroup(
      Rectangle(fill_opacity=1, fill_color=BLACK),
      PTex("R_x(6.07)"),
    )
    u_gate_11[0].surround(u_gate_11[1], stretch=True)
    d_gate_11 =  VGroup(
      Rectangle(fill_opacity=1, fill_color=BLACK),
      PTex("R_x(4.39)"),
    )
    d_gate_11[0].surround(d_gate_11[1], stretch=True)
    # GATE 2
    u_gate_2 = Dot().scale(2).shift(UP)
    d_gate_2 = Dot(fill_opacity=0, stroke_opacity=3, stroke_width=4).scale(2).shift(DOWN)
    line_gate_2 = Line(UP, DOWN)
    line_gate_2.add_updater(
      lambda mob: mob.put_start_and_end_on(u_gate_2.get_bottom(), d_gate_2.get_bottom())
    )
    line_gate_2.add_updater(
      lambda mob: mob.set_opacity(
        1 if mob.get_x() > phantom_bk.get_left()[0]
          else 0
      )
    )
    # Gate 3
    u_gate_3 = Gate3()
    d_gate_3 = Gate3()

    """
    Mask animation utils
    """

    def mask_closure(mob, slider):
      mob_target = mob.copy()
      mob_target.next_to(slider, LEFT, buff=0.1).align_to(mob, UP)
      target = mob_target.get_center()
      vector = target - mob.get_center()
      return lambda m, a: m.shift(vector[0]* RIGHT * a)

    def mask_anim(mob, slider, bk, rate_func=linear, **kwargs):
      return self.mask_anim(
        mob, bk,
        mask_closure(mob, slider),
        rate_func=rate_func,
        **kwargs
      )

    black_line = Line(
      phantom_bk.get_corner(UL),
      phantom_bk.get_corner(DL),
      color=BLACK,
      stroke_width=5
    )

    # a1 = qbit.get_arrow(RIGHT).set_color(ORANGE)
    self.add(phantom_bk)
    self.add_foreground_mobject(black_line)
    self.add(
      u_qbit, d_qbit,
      u_arrow, d_arrow, 
      u_slider, d_slider,
      _G1, _G2,
      u_EQUAL, d_EQUAL,
      u_formula_1, d_formula_1
    )
    # =====================
    # ANIMATIONS
    # =====================
    # ---- Gate 1
    self.play(
      self.show_gate(u_gate_1, u_slider),
      self.show_gate(d_gate_1, d_slider),
    )
    self.wait()
    self.play(
      # Pop Gates
      u_gate_1.animate(rate_func=there_and_back).scale(1.4),
      d_gate_1.animate(rate_func=there_and_back).scale(1.4),
      # Rotate vectors
      Rotate(
        u_arrow,
        imbedding_u,
        about_point=u_qbit.circle.get_center(),
        rate_func=linear
      ),
      Rotate(
        d_arrow,
        imbedding_d,
        about_point=d_qbit.circle.get_center(),
        rate_func=linear
      ),
      # Change states
      FadeOut(u_formula_1, rate_func=linear),
      FadeIn(u_formula_11, rate_func=linear),
      FadeOut(d_formula_1, rate_func=linear),
      FadeIn(d_formula_11, rate_func=linear),
      run_time=2
    )
    self.wait()
    # another set of rotation gates
    self.play(
      mask_anim(u_gate_1, u_slider, phantom_bk, run_time=2),
      mask_anim(d_gate_1, d_slider, phantom_bk, run_time=2),
      AnimationGroup(
        Wait(1.2),
        self.show_gate(u_gate_11, u_slider, run_time=1.5),
        lag_ratio=1,
      ),
      AnimationGroup(
        Wait(1.2),
        self.show_gate(d_gate_11, d_slider, run_time=1.5),
        lag_ratio=1,
      ),
    )

    self.play(
      # Pop Gates
      u_gate_11.animate(rate_func=there_and_back).scale(1.4),
      d_gate_11.animate(rate_func=there_and_back).scale(1.4),
      # Rotate
      Rotate(
        u_arrow,
        weight_u,
        about_point=u_qbit.circle.get_center(),
        rate_func=linear
      ),
      Rotate(
        d_arrow,
        weight_d,
        about_point=d_qbit.circle.get_center(),
        rate_func=linear
      ),
      # Change states
      FadeOut(u_formula_11, rate_func=linear),
      FadeIn(u_formula_2, rate_func=linear),
      FadeOut(d_formula_11, rate_func=linear),
      FadeIn(d_formula_2, rate_func=linear),
      run_time=2
    )
    self.wait()
    """
    Gate 1 to Gate 2
    """
    self.add(line_gate_2)
    O_TIMES = MathTex(r"\otimes",font_size=FONT_SIZE)
    G_grp_1 = VGroup(_G1, _G2)
    G_grp_1.generate_target()
    G_grp_1.target.arrange(RIGHT, buff=1)\
        .align_to(_G1, LEFT)\
        .shift(LEFT*1.5)
    u_EQUAL.generate_target()
    u_EQUAL.target.next_to(G_grp_1.target, RIGHT, buff=0.3)
    O_TIMES.move_to(G_grp_1.target)
    formula_1 = VGroup(
      # MathTex("-i"),
      Matrix([
        [-0.02],
        ["0.52i"],
        ["0.03i"],
        ["0.85"]
      ])
    )   .arrange(RIGHT, buff=0.3)\
        .next_to(u_EQUAL.target, RIGHT, buff=0.3)
    formula_2 = VGroup(
      # MathTex("-i"),
      Matrix([
        [-0.02],
        ["0.52i"],
        ["0.85"],
        ["0.03i"]
      ])
    )   .arrange(RIGHT, buff=0.3)\
        .next_to(u_EQUAL.target, RIGHT, buff=0.3)
    d_arrow_2 = d_qbit.get_arrow(UP).set_opacity(0.5)
    d_arrow_2.set_color(PURPLE)
    d_arrow_2.tip.set_stroke(width=0)
    u_arrow_2 = u_qbit.get_arrow(DOWN).set_opacity(0.5)
    u_arrow_2.set_color(PURPLE)
    u_arrow_2.tip.set_stroke(width=0)
    # Animations ------------
    self.play(
      mask_anim(u_gate_11, u_slider, phantom_bk),
      mask_anim(d_gate_11, d_slider, phantom_bk),
      AnimationGroup(
        Wait(1),
        self.show_gate(u_gate_2, u_slider),
        lag_ratio=1,
      ),
      AnimationGroup(
        Wait(1),
        self.show_gate(d_gate_2, d_slider),
        lag_ratio=1,
      ),
      # Move formula q1 q2
      MoveToTarget(G_grp_1),
      MoveToTarget(u_EQUAL),
      Transform(d_EQUAL, u_EQUAL.target, remover=True),
      AnimationGroup(
        Wait(1),
        Write(O_TIMES),
        lag_ratio=1,
      ),
      # Fade out matrix up and down
      FadeOut(u_formula_2),
      FadeOut(d_formula_2),
      # Write new formula
      AnimationGroup(
        Wait(1),
        Write(formula_1),
        lag_ratio=1,
      ),
      run_time=2
    )
    self.wait()
    self.play(
      # GLOW animation on qbit
      u_qbit.circle.animate(rate_func=there_and_back)
        .set_style(stroke_color=YELLOW, stroke_width=15),
      d_qbit.circle.animate(rate_func=there_and_back)
        .set_style(stroke_color=YELLOW, stroke_width=15),
      # Transform matrix
      FadeOut(formula_1, rate_func=linear),
      FadeIn(formula_2, rate_func=linear),

      # TransformMatchingShapes(
      #   formula_1, formula_2
      # ),

      FadeIn(d_arrow_2),
      run_time=2
    )
    """
    Gate 2 to Gate 3
    """
    self.play(
      mask_anim(u_gate_2, u_slider, phantom_bk, run_time=2),
      mask_anim(d_gate_2, d_slider, phantom_bk, run_time=2),
      AnimationGroup(
        Wait(1.2),
        self.show_gate(u_gate_3, u_slider, run_time=1.5),
        lag_ratio=1,
      ),
      AnimationGroup(
        Wait(1.2),
        self.show_gate(d_gate_3, d_slider, run_time=1.5),
        lag_ratio=1,
      ),
    )
    self.remove(u_gate_2, d_gate_2, line_gate_2)
    self.wait()
    self.play(
      ReplacementTransform(u_arrow, u_arrow_2),
      ReplacementTransform(d_arrow, d_arrow_2),
      run_time=2
    )
    self.wait()


# to run manim -p -qm --disable_caching qbit_animation.py MainScene