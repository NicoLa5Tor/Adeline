class Functions:
    def __init__(self,w = [],list_logical = []) -> None:
        self.logical  =list_logical
    def sum_net(self,index):
        z_toria = 0
        ind = 0
        com_logical_reverse = self.logical[index][::-1]
        while ind < len(self.logical)-1:
            z_toria += com_logical_reverse[ind+1] * self.list_w[ind]
            ind += 1
        return z_toria