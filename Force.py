class Force:
    def __init__(self,r1=0,r2=0,r3=0):
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self._components = [self.r1, self.r2, self.r3]

    def getComponent(self, i):
        return self._components[i]

    def ForcePrint(self):
        print(self._components)
