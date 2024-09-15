class Functions:
    def __init__(self,w = [],list_logical = [],alpha = 0.5):
        self.logical  =list_logical
        self.list_w = w
        self.alpha = alpha
    def sum_net(self,index):
        com_logical_reverse = self.logical[index][::-1]
        #print(com_logical_reverse)
        return sum(com_logical_reverse[i+1] * self.list_w[i] for i in range(len(self.list_w)))
    def new_w(self,index,Yop):
        list_actual = self.logical[index][::-1]
        yd = list_actual[0]
        mag_error = yd - Yop
        return [
            self.list_w[i] + (self.alpha * mag_error * list_actual[i+1]) for i in range(len(self.list_w))
        ]
    def magnitud(self,dat):
        return dat if dat > 0 else dat * -1


