import numpy as np
import functools

class Unit:
    def __init__(self,_size,_matrix=0):
        self.id=-1
        self.size=_size
        if _matrix:
            self.matrix=_matrix
        else:
            self.matrix =np.zeros((self.size,self.size))

    def setMatrix(self,_matrix):
        _matrix=np.matrix(_matrix)
        if _matrix.shape[0] != self.size:
            print(f"Update failed. Input matrix does not have a shape of ({self.size}, {self.size})")
            return 0
        self.matrix=_matrix
        return 1

    def setID(self,_id):
        self.id=_id

    def getMatrix(self):
        return self.matrix

    def getSize(self):
        return self.size

    def __str__(self):
        return f'id: {self.id}\r size:{self.size}\r QUBO matrix:\r{self.matrix}'


class QUBO:
    def __init__(self,_units=[]):
        self.currentIndex=0 #当前子QUBO编号数，从0开始，总子QUBO数为这个值+1
        self.subquboList=_units
        self.matrix = self.unitsHandler(self.subquboList)
        self.coherence=[]

    def unitsHandler(self,_units):
        if _units==[]:
            return 0
        totalMatrix=_units[0].getMatrix()
        for aunit in _units:
            if self.currentIndex:
                oriLength=totalMatrix.shape[0]
                nrow = np.zeros((aunit.getSize(), oriLength))
                totalMatrix = np.r_[totalMatrix, nrow]
                ncol=np.zeros((oriLength,aunit.getSize()))
                ncol = np.r_[ncol, aunit.getMatrix()]
                totalMatrix = np.c_[totalMatrix, ncol]
            aunit.setID(self.currentIndex)
            self.currentIndex+=1
        return totalMatrix

    @functools.lru_cache()
    def getPosition(self,_unit,_partical):
        position=0
        for id in range(_unit):
            position+=self.subquboList[id].getSize()
        position+=_partical-1#(start from 0)
        return position

    def add(self,_newunit):
        self.subquboList.append(_newunit)
        self.matrix = self.unitsHandler(self.subquboList)

    def updateCoherence(self,_unit1,_partical1,_unit2,_partical2,_coherenceFactor):
        self.coherence.append([_unit1,_partical1,_unit2,_partical2])
        position1=self.getPosition(_unit1,_partical1)
        position2 = self.getPosition(_unit2, _partical2)
        self.matrix[position1,position2]=_coherenceFactor
        self.matrix[position2,position1]=_coherenceFactor

    def decoherence(self,_unit1,_partical1,_unit2,_partical2):
        self.updateCoherence(_unit1,_partical1,_unit2,_partical2,0)

    def __str__(self):
        return f'subquboList: {self.subquboList}\r size:{self.currentIndex+1}\r QUBO matrix:\r{self.matrix}\r coherence:{self.coherence}'


a1=Unit(3)
a1.setMatrix([[0,1,0],[1,0,0],[0,0,0]])
a2=Unit(4)
a2.setMatrix([[0,2,1,2],[2,0,1,1],[1,1,0,1.5],[2,1,1.5,0]])
print(a2)
a3=Unit(2)
a3.setMatrix([[0,0.5],[0.5,0]])

myqubo=QUBO([a1,a2,a3])
myqubo.add(a1)
myqubo.updateCoherence(0,2,1,3,10)
myqubo.updateCoherence(0,3,1,2,10)
myqubo.updateCoherence(2,2,1,3,20)
print(myqubo)