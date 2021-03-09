class Pile:
    a = []
    index = 0
    
    def __init__(self,taille):
        self.taille = taille
        self.a = [0 for i in taille]

    def push(self, entite):
        self.a[self.index] = entite
        self.index += 1

    def pop(self):
        b = self.a[self.index]
        self.index -= 1
        return b

class File:
    a = []
    index = 0
    i2 = 0

    def __init__(self,taille):
        self.taille = taille
        self.a = [0 for i in taille]
    
    def push(self, entite):
        self.a[self.i2] = entite
        self.i2 += 1
    
    def pop(self, entite):
        b = self.a[self.index]
        self.index += 1
        return b