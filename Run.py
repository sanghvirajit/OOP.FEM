from Structure import *
from Constraint import *
from Force import *
from myViewer import *

Structure = Structure()

lb = 15.0
r = 457.2 / 2000
t = 10.0 / 1000
a = math.pi * (math.pow(r, 2) - math.pow(r - t, 2))
e = 2.1e11

c1 = Constraint(False, False, False)
c2 = Constraint(True, True, False)

F = Force(0, -20e3, -100e3)

n1 = Structure.addNode(0.0, 0.0, lb * math.sqrt(2.0/3.0))
n2 = Structure.addNode(0.0, lb / math.sqrt(3), 0.0)
n3 = Structure.addNode(-lb / 2, -lb / math.sqrt(12.0), 0.0)
n4 = Structure.addNode(lb/2, -lb / math.sqrt(12.0), 0.0)

n1.setForce(F)
n2.setConstraint(c1)
n3.setConstraint(c1)
n4.setConstraint(c2)


e1 = Structure.addElement(e, a, n1, n2)
e2 = Structure.addElement(e, a, n1, n3)
e3 = Structure.addElement(e, a, n1, n4)
e4 = Structure.addElement(e, a, n2, n3)
e5 = Structure.addElement(e, a, n3, n4)
e6 = Structure.addElement(e, a, n4, n2)

Structure.printStructure()
Structure.Solve()
Structure.printResults()

Viewer = MyViewer(Structure)
Viewer.draw_elements()
Viewer.draw_constraint()
Viewer.draw_element_forces()
Viewer.draw_displacement()
Viewer.draw_nodal_force()
Viewer.run()
