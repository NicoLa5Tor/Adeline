import random as rm
class Operations:
    def __init__(self,cant = 3) -> None:
        self.iteration = cant
    def w(self):
       return [round(rm.uniform(-1,1),2) for _ in range(self.iteration)]