#!/usr/bin/python

from boxes import Boxes
import math

class Lamp(Boxes):
    def __init__(self):
        Boxes.__init__(self, width=1000, height=1000)
        self.fingerJointSettings = (5, 5)

    def ring(self, r, w):
        self.ctx.save()
        d = 2*(r+w)
        self.roundedPlate(d, d, r)

        self.moveTo(r+w, w)
        self.corner(360, r)
        self.ctx.restore()

    def roundedTriangle(self, length, angle, r=0.0):
        x = 0.5*(length-2*r)*math.tan(math.radians(angle))
        y =  0.5*(length)
        self.hole(x, y, 2)
        l = 0.5 * (length-2*r) / math.cos(math.radians(angle))
        self.corner(90-angle, r)
        self.edge(l)
        self.corner(2*angle, r)
        self.edge(l)
        self.corner(90-angle, r)

    def side(self, y, h):
        self.fingerJoint(y)
        self.corner(90)
        self.fingerJoint(h)
        self.roundedTriangle(y, 70, 25)
        self.fingerJoint(h)
        self.corner(90)

    def render(self, r, w, x, y, h):
        """
        r : radius of lamp
        w : width of surrounding ring
        """
        d = 2*(r+w)
        self.ctx.save()
        self.moveTo(20, 20)
        self.ring(r, w)
        self.moveTo(2*(r+w)+20, 0)
        self.roundedPlate(d, d, r, holesMargin=w/2.0)

        self.ctx.restore()
        self.moveTo(10, 2*(r+w)+40)
        self.surroundingWall(d, d, r, 150, top='h', bottom='h')
        self.moveTo(0, 150+20)

        self.rectangularWall(x, y, edges="fFfF", holesMargin=5)
        self.moveTo(x+20, 0)
        self.rectangularWall(x, y, edges="fFfF", holesMargin=5)
        self.moveTo(x+20, 0)
        self.side(y, h)
        self.moveTo(y+20, 0)
        self.side(y, h)

        self.moveTo(0, y+20)
        self.moveTo(-x-y-40, 0)
        self.rectangularWall(x, h, edges='hFFF', holesMargin=5)
        self.moveTo(-x-20, 0)
        self.rectangularWall(x, h, edges='hFFF', holesMargin=5)

        self.ctx.stroke()
        self.surface.flush()


l = Lamp()
l.render(100, 20, 250, 140, 120)
