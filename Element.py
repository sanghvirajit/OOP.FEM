from numpy import outer, block, transpose, dot, array
from numpy.linalg import norm
from math import sqrt


class Element:
    def __init__(self, e, a, n1, n2):
        self._eModulus = e
        self._area = a
        self.n1 = n1
        self.n2 = n2
        self._dofNumbers = []

    def computeStiffnessMatrix(self):
        coeff = self._eModulus * self._area / self.getLength()**3
        a = outer(self.n2.getPosition() - self.n1.getPosition(), self.n2.getPosition() - self.n1.getPosition())
        b = -outer(self.n2.getPosition() - self.n1.getPosition(), self.n2.getPosition() - self.n1.getPosition())
        c = -outer(self.n2.getPosition() - self.n1.getPosition(), self.n2.getPosition() - self.n1.getPosition())
        d = outer(self.n2.getPosition() - self.n1.getPosition(), self.n2.getPosition() - self.n1.getPosition())
        return coeff*block([[a, b], [c, d]])

    def enumerateDOFs(self):
        self.n1.getDOFNumbers()
        self.n2.getDOFNumbers()

    def getDOFNumbers(self):
        self._dofNumbers = array([array(self.n1.getDOFNumbers()), array(self.n2.getDOFNumbers())]).flatten()
        return self._dofNumbers

    def computeForce(self):
        T = self.getT()
        u1 = dot(T, self.getNode1().getDisplacement())
        u2 = dot(T, self.getNode2().getDisplacement())
        eps11 = (u2 - u1)
        return (self._eModulus * self._area / self.getLength()) * eps11

    def getT(self):
        T = transpose(self.n2.getPosition() - self.n1.getPosition()) / (norm(self.n2.getPosition() - self.n1.getPosition(), 2))
        return T

    def getLength(self):
        l = self.n1.getPosition() - self.n2.getPosition()
        return sqrt(dot(l,l))

    def getNode1(self):
        return self.n1

    def getNode2(self):
        return self.n2

    def getArea(self):
        return self._area

    def geteModulus(self):
        return self._eModulus

    def ElementPrint(self):
        print(str(self._eModulus) ,'\t\t\t', str(self._area), '\t\t\t', str(self.getLength()))
