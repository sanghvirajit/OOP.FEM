from Element import *
from Node import *
from decimal import *
from numpy.linalg import solve


class Structure:
    def __init__(self):
        self.Elements = []
        self.Nodes = []

    def addNode(self, x1, x2, x3):
        self.Nodes.append(Node(x1, x2, x3))
        return self.Nodes[-1]

    def addElement(self, e, a, n1, n2):
        self.Elements.append(Element(e, a, n1, n2))
        return self.Elements[-1]

    def getNumberOfNodes(self):
        return len(self.Nodes)

    def getNode(self, a):
        return self.Nodes[a]

    def getNumberOfElements(self):
        return len(self.Elements)

    def getElement(self, a):
        return self.Elements[a]

    def printStructure(self):
        counter = 0

        print('\n')
        print("Node Positions")
        print("idx\t", "x1 \t\t\t", "x2 \t\t\t", "x3")
        for i in self.Nodes:
            print(counter, "\t",
                  '%.4E' % Decimal(i.getPosition()[0]), "\t",
                  '%.4E' % Decimal(i.getPosition()[1]), "\t",
                  '%.4E' % Decimal(i.getPosition()[2]))
            counter += 1

        counter = 0

        print('\n')
        print("Constraint")
        print("idx\t", "x \t\t", "y \t\t", "z")
        for i in self.Nodes:
            print(counter, end="\t")
            i.getConstraint().ConstraintPrint()
            counter += 1

        counter = 0

        print('\n')
        print("Force Components")
        print("idx\t", "u1 \t\t\t", "u2 \t\t\t", "u3")
        for i in self.Nodes:
            print(counter, "\t",
                  '%.4E' % Decimal(i.getForce().getComponent(0)), "\t",
                  '%.4E' % Decimal(i.getForce().getComponent(1)), "\t",
                  '%.4E' % Decimal(i.getForce().getComponent(2)))
            counter += 1


        counter = 0

        print('\n')
        print("Elements")
        print("idx\t", "eModulus\t", "Area \t\t", "length")
        for i in self.Elements:
            print(counter, end ="\t")
            i.ElementPrint()
            print("\t\t")
            counter += 1

    def Solve(self):
        DOF = self.enumerateDOFs()
        A = self.assembleStiffnessMatrix(zeros([DOF, DOF]))
        b = self.assembleLoadVector(zeros([DOF]))
        print('Kglobal',"\n\n", A)
        print("\n")
        print('Fglobal', "\n\n", b)
        self.d = solve(A,b)
        self.selectDisplacement()
        return self.d


    def enumerateDOFs(self):
        start = 0
        for i in self.Nodes:
            start = i.enumerateDOFs(start)
        for j in self.Elements:
            j.enumerateDOFs()
        return start

    def assembleLoadVector(self, rglob):
        for i in self.Nodes:
            for j in range(3):
                if i.getConstraint().isFree(j):
                    rglob[i.getDOFNumbers()[j]] += i.getForce().getComponent(j)
        return rglob


    def assembleStiffnessMatrix(self, kglob):
        for i in self.Elements:
            for j in range(6):
                for k in range(6):
                    if (i.getDOFNumbers()[j] >= 0) and (i.getDOFNumbers()[k] >= 0):
                        kglob[i.getDOFNumbers()[j], i.getDOFNumbers()[k]] += i.computeStiffnessMatrix()[j, k]
        return kglob

    def selectDisplacement(self):
        for i in self.Nodes:
            DOF = i.getDOFNumbers()
            u = []
            for j in DOF:
                if j >= 0:
                    u.append((self.d[j]))
                else:
                    u.append(0)
            i.setDisplacement(u)

    def printResults(self):

        counter = 0
        print('\n')
        print("Displacement Components")
        print("idx\t", "u1 \t\t\t", "u2 \t\t\t", "u3")
        for i in self.Nodes:
            print(counter, "\t",
                  '%.4E' % Decimal(i.getDisplacement()[0]), "\t",
                  '%.4E' % Decimal(i.getDisplacement()[1]), "\t",
                  '%.4E' % Decimal(i.getDisplacement()[2]))
            counter += 1


        counter = 0
        print('\n')
        print("Element Force")
        print("idx\t" , "force")
        for i in self.Elements:
            print(counter, "\t",
                  '%.4E' % Decimal(str(i.computeForce())))
            counter += 1



