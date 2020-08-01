from pview3d import *
from math import sqrt, pi
from numpy import array, cross, log10, count_nonzero
from numpy.linalg import norm


class MyViewer:

    def __init__(self, structure):
        self.Structure = structure
        self.symbolScale = 1
        self.nodal_force_scale = 1e-3
        self.element_force_symbol_scale = 3e-5
        self.displacementScale = 1
        self.Viewer = Viewer()

    def draw_elements(self):
        cs = CylinderSet()
        cs.color = 'antiquewhite'

        for i in self.Structure.Elements:
            area = i.getArea()
            r = area / pi
            cs.add_cylinder(i.getNode1().getPosition(), i.getNode2().getPosition(), sqrt(r))
        self.Viewer.add_object(cs)

    def draw_constraint(self):
        for i in self.Structure.Nodes:
            for j in range(3):
                if i.getConstraint().isFree(j) == False:

                    c = Cone()
                    if j == 0:
                        c.direction = self.symbolScale * [1, 0, 0]
                        c.center = i.getPosition() - array([c.height, 0, 0])
                        c.color = 'red'
                    elif j == 1:
                        c.direction = self.symbolScale * [0, 1, 0]
                        c.center = i.getPosition() - array([0, c.height, 0])
                        c.color = 'green'
                    elif j == 2:
                        c.direction = self.symbolScale * [0, 0, 1]
                        c.center = i.getPosition() - array([0, 0, c.height])
                        c.color = 'blue'

                    c.radius = self.symbolScale * 0.25
                    c.height = self.symbolScale * 1
                    c.radius = self.symbolScale * 0.5
                    self.Viewer.add_object(c)

    def draw_element_forces(self):
        for i in self.Structure.Elements:
            d = (i.getNode2().getPosition() - i.getNode1().getPosition()) / norm(
                (i.getNode2().getPosition() - i.getNode1().getPosition()), 2)
            n2 = cross(d, array([0, 0, 1]))
            p = cross(n2, d)

            s1 = i.getNode1().getPosition() + self.element_force_symbol_scale * i.computeForce() * p
            s2 = i.getNode2().getPosition() + self.element_force_symbol_scale * i.computeForce() * p

            ps = PolygonSet()

            ps.insert_vertex(s1[0], s1[1], s1[2], 0)
            ps.insert_vertex(s2[0], s2[1], s2[2], 1)

            ps.insert_vertex(i.getNode2().getPosition()[0], i.getNode2().getPosition()[1],
                             i.getNode2().getPosition()[2], 2)
            ps.insert_vertex(i.getNode1().getPosition()[0], i.getNode1().getPosition()[1],
                             i.getNode1().getPosition()[2], 3)
            ps.polygon_complete()

            ps.color_by_data = True
            ps.outlines_visible = True
            ps.create_colors()
            self.Viewer.add_object(ps)

    def draw_nodal_force(self):
        cs = CylinderSet()
        cs.color = 'blue'
        for i in self.Structure.Nodes:
            force = i.getForce()
            force = array([force.getComponent(0), force.getComponent(1), force.getComponent(2)])
            if count_nonzero(force) != 0:
                force_norm = force / norm(force, 2)
                cone = Cone()
                cone.direction = force / norm(force, 2)
                cone.color = 'blue'
                cone.height = self.symbolScale * 1
                cone.center = i.getPosition() - cone.height * cone.direction
                cs.add_cylinder(i.getPosition() - force_norm * cone.height, i.getPosition() - (force_norm * 5)
                                * self.symbolScale, self.symbolScale * 0.1)
                self.Viewer.add_object(cone)
        self.Viewer.add_object(cs)

    def draw_displacement(self):
        scale = log10(abs(self.Structure.d))
        scale = abs(scale)
        scale = 10 ** (scale.min())
        self.displacementScale = scale
        cs = CylinderSet()
        cs.color = 'green'

        for i in self.Structure.Elements:
            area = i.getArea()
            r = area / pi
            a1 = i.getNode1().getPosition()[0] + self.displacementScale * i.getNode1().getDisplacement()[0]
            a2 = i.getNode1().getPosition()[1] + self.displacementScale * i.getNode1().getDisplacement()[1]
            a3 = i.getNode1().getPosition()[2] + self.displacementScale * i.getNode1().getDisplacement()[2]
            a = array([a1, a2, a3])

            b1 = i.getNode2().getPosition()[0] + self.displacementScale * i.getNode2().getDisplacement()[0]
            b2 = i.getNode2().getPosition()[1] + self.displacementScale * i.getNode2().getDisplacement()[1]
            b3 = i.getNode2().getPosition()[2] + self.displacementScale * i.getNode2().getDisplacement()[2]
            b = array([b1, b2, b3])

            cs.add_cylinder(a, b, sqrt(r))
        self.Viewer.add_object(cs)

    def run(self):
        self.Viewer.run()
