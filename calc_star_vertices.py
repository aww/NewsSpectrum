#!/usr/bin/env python

from math import pi, sin, cos, tan

points = 5
angle_step = pi / points # angle between two vertices, one outer, one inner
outer_r = 1.0
inner_r = outer_r * sin(pi/2 - 2*angle_step) / cos(angle_step)
inner_r *= 1.4

area = points * tan(angle_step) * sin(pi/2 - 2*angle_step)
print "Area is", area
print "Scale factor would be", pi / area

for i in range(points):
    angle = i * 2 * angle_step - pi / 2
    print "%.4f,%.4f " % (outer_r * cos(angle), outer_r * sin(angle)),
    angle = (i * 2 + 1) * angle_step - pi / 2
    print "%.4f,%.4f " % (inner_r * cos(angle), inner_r * sin(angle)),

