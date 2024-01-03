# Copyright (C) 2013-2014 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import *


class BinFrontEdge(edges.BaseEdge):
    char = "B"
    def __call__(self, length, **kw):
        f = self.settings.front
        a1 = math.degrees(math.atan(f/(1-f)))
        a2 = 45 + a1
        self.corner(-a1)
        # l = self.settings.y
        l = length
        self.edges["e"](l* (f**2+(1-f)**2)**0.5)
        self.corner(a2)            
        self.edges["f"](l*f*2**0.5)
        self.corner(-45)

    def margin(self) -> float:
        return self.settings.y * self.settings.front

class BinFrontSideEdge(BinFrontEdge):
    char = 'b'

class StackableTray(Boxes):
    """A stackable type tray variant with sloped walls in front"""

    ui_group = "Shelf"

    def __init__(self) -> None:
        Boxes.__init__(self)
        self.addSettingsArgs(edges.StackableSettings)
        self.buildArgParser("sx", "y", "h", "hi", "outside")
        self.addSettingsArgs(edges.FingerJointSettings, surroundingspaces=0.5)
        self.argparser.add_argument(
            "--front", action="store", type=float, default=0.4,
            help="fraction of bin height covered with slope")


    def ySlots(self):
        posy = -0.5 * self.thickness
        # for y in self.sy[:-1]:
        posy += self.y + self.thickness
        posy = self.bottom_offset
        posx = 0
        for x in self.sx:
            self.fingerHolesAt(posy, posx, x)
            posx += x + self.thickness
    
    def xSlots(self):
        posx = -0.5 * self.thickness
        posy = self.bottom_offset
        for x in self.sx[:-1]:
            posx += x + self.thickness            
            self.fingerHolesAt(posx, posy, self.yi)
        

    def xHoles(self):
        posx = -0.5 * self.thickness
        for x in self.sx[:-1]:
            posx += x + self.thickness
            self.fingerHolesAt(posx, 0, self.hi)
            
    def frontHoles(self, i):
        def CB():
            posx = -0.5 * self.thickness
            for x in self.sx[:-1]:
                posx += x + self.thickness
                self.fingerHolesAt(posx, 0, self.yi*self.front*2**0.5)
        return CB

    def yHoles(self):
        posy = self.bottom_offset
        self.fingerHolesAt(posy, 0, self.hi)

    def render(self):
        if self.outside:
            self.sx = self.adjustSize(self.sx)
            self.y = self.adjustSize(self.y)
            self.h = self.adjustSize(self.h, e2=False)

        x = sum(self.sx) + self.thickness * (len(self.sx) - 1)
        y = self.y

        # bottom_edge = "š" if self.stackable else "e"
        # top_edge = "S" if self.stackable else "e"
        self.bottom_offset =  0.5 * self.thickness + self.edges["š"].settings.holedistance
            
        h = self.h
        if self.hi:
            yi = self.yi = self.hi - self.bottom_offset
        else:
            yi = self.yi = y - self.bottom_offset

        hi = self.hi = h
        
        t = self.thickness
        self.front = min(self.front, 0.999)

        self.addPart(BinFrontEdge(self, self))
        self.addPart(BinFrontSideEdge(self, self))

        angledsettings = copy.deepcopy(self.edges["f"].settings)
        angledsettings.setValues(self.thickness, True, angle=45)
        angledsettings.edgeObjects(self, chars="gGH")

        # outer walls
        e = ["F", "f", edges.SlottedEdge(self, self.sx[::-1], "G"), "f"]

        self.rectangularWall(x, h, e, callback=[self.xHoles],  move="right", label="bottom")
        self.rectangularWall(y, h, "FSbš", callback=[self.yHoles], move="up", label="left")
        self.rectangularWall(y, h, "FSbš", callback=[self.yHoles], label="right")
             
        self.rectangularWall(x, y, "šfSf", callback=[self.xSlots, self.ySlots], move="left", label="back")
        self.rectangularWall(y, h, "FFBF", move="up only")
        # front wall
        e = [edges.SlottedEdge(self, self.sx, "g"), "F", "e", "F"]
        self.rectangularWall(x, y*self.front*2**0.5, e, callback=[self.frontHoles(0)], move="up", label="retainer")

   
        # Inner walls
        for i in range(len(self.sx) - 1):
            e = [edges.SlottedEdge(self, [yi], "f"), "e", "B", "f"]            
            self.rectangularWall(yi, hi, e, move="up", label="inner vertical " + str(i+1))

        
