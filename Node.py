from Force import *
from Constraint import *
from numpy import *

class Node:
    def __init__(self, x1, x2, x3):
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self._dofNumbers = []
        self._Force = Force()
        self._Constraint = Constraint(True, True, True)
        self._displacement = zeros(3)
        self._position = array([self.x1, self.x2, self.x3])

    def setConstraint(self, constraint):
        self._Constraint = constraint

    def getConstraint(self):
        return self._Constraint

    def setForce(self, force):
        self._Force = force

    def getForce(self):
        return self._Force

    def enumerateDOFs(self, start):
        for i in range(3):
            if self._Constraint.isFree(i):
                self._dofNumbers.append(start)
                start += 1
            else:
                self._dofNumbers.append(-1)
        return start

    def getDOFNumbers(self):
        return self._dofNumbers

    def getPosition(self):
        return array([self.x1, self.x2, self.x3])

    def setDisplacement(self, u):
        self._displacement[0] = u[0]
        self._displacement[1] = u[1]
        self._displacement[2] = u[2]

    def getDisplacement(self):
        return self._displacement

    def NodePrint(self):
        print(self._position)
