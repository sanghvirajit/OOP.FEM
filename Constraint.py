class Constraint:
    def __init__(self, dof1=True, dof2=True, dof3=True):
        self.dof1 = dof1
        self.dof2 = dof2
        self.dof3 = dof3
        self._free = [self.dof1 , self.dof2 , self.dof3]

    def constraint(self, u1, u2, u3):
        self.dof1 = u1
        self.dof2 = u2
        self.dof3 = u3

    def isFree(self, i):
        return self._free[i]

    def ConstraintPrint(self):
        u1, u2, u3 = "fixed", "fixed", "fixed"
        if self.isFree(0):
            u1 = "free"
        if self.isFree(1):
            u2 = "free"
        if self.isFree(2):
            u3 = "free"
        return print(u1, "\t", u2, "\t", u3)
