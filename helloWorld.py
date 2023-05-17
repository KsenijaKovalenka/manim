from manim import *

# CONFIG dict
# config.preview = True

class HelloWorld(Scene):
    def construct(self):
        hw = Text("Hello world")
        self.play(Write(hw))
        self.wait()

r"""
==================
Preview
==================

Open your default video media player

-p

==================
Render options
==================

-q + RESOLUTION FLAG:

-ql = low resolution:     480p  15 fps
-qm = medium resolution:  720p  15 fps
-qh = hight resolution:   1080p 15 fps
-qp = 2k resolution:      1440p 15 fps
-qk = 4k resolution:      2160p 15 fps

============
Set fps
============

--fps=FPS

Example: --fps=25

===================
Custom resolution
===================

-r WIDTH,HEIGHT

Example: -r 500,500

================
Transparency
================

PNG with transparency or MOV video file with alpha channel

-t

===========================
Save last frame as image
===========================

-s

Example: Save last frame with transparency:

-ts

======================
Settings Priority
======================

manim.cfg < CLI < CONFIG dict

--disable_caching (use always)

"""