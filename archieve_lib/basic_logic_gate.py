from sim import *



class And:

    def __init__(self, in_len=2) -> None:
        self.__input = [N for _ in range(in_len)]
        self.__output = N

        self.__change_flag = True
        self.elements = self.input


    def netlist(self):
        if X in self.input:
            self.__output = X
            return
        _input = [i for i in self.input if i in (L, H)]
        if len(_input) == 0:    # all of inputs are N
            self.__output = N
            return
        self.__output = all(_input)
        

    @property
    def input(self):
        return self.__input
    

    @input.setter
    def input(self, value):
        self.__input = value


    @property
    def output(self):
        self.__change_flag = False
        self.netlist()
        return self.__output

    
    @property
    def change_flag(self):
        return self.__change_flag
    

x = And(2)
x.input[0] = H
x.input[1] = H

print(x.output)