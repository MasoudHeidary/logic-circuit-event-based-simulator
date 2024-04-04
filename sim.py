import func

DEBUG = False

# valid values '1'(1), '0'(0), 'x'(2), 'n'(3)

L = 0
H = 1
X = 2
N = 3


class NMOS:
    def __init__(self) -> None:
        self.__input = N
        self.__gate = N
        self.__change_flag = True
        self.__output = N

    @property
    def change_flag(self):
        return self.__change_flag
    
    @property
    def input(self):
        return self.__input
    
    @input.setter
    def input(self, value):
        if(self.__input != value):
            self.__change_flag = True
        self.__input = value

    @property
    def gate(self):
        return self.__gate
    
    @gate.setter
    def gate(self, value):
        if(self.__gate != value):
            self.__change_flag = True
        self.__gate = value


    def __get_output(self):
        if self.gate == H:
            return self.input
        if self.gate == L:
            return N
        return self.gate

    @property
    def output(self):
        self.__change_flag = False
        self.__output = self.__get_output()
        return self.__output
        
    
    def __repr__(self) -> str:
        return f"{self.input} {self.gate} => {self.__get_output()}, {self.change_flag}"


class PMOS:
    def __init__(self, input=N, gate=N) -> None:
        self.__input = input
        self.__gate = gate
        self.__change_flag = True
        self.__output = N


    @property
    def change_flag(self):
        return self.__change_flag
    
    @property 
    def input(self):
        return self.__input
    
    @input.setter
    def input(self, value):
        if(self.__input != value):
            self.__change_flag = True
        self.__input = value
    
    @property
    def gate(self):
        return self.__gate

    @gate.setter
    def gate(self, value):
        if(self.__gate != value):
            self.__change_flag = True
        self.__gate = value

    def __get_output(self):
        if self.gate == L:
            return self.input
        if self.gate == H:
            return N
        return self.gate

    @property
    def output(self):
        self.__change_flag = False
        self.__output = self.__get_output()
        return self.__output
    
    def __repr__(self) -> str:
        return f"{self.input} {self.gate} => {self.__get_output()}, {self.change_flag}"


    
class Wire:
    def __init__(self, in_len = 1) -> None:
        self.__input = [N] * in_len
        self.__change_flag = True
        self.__output = N


    # get value of inputs
    def __getitem__(self, index):
        return self.__input[index]

    # change value of inputs
    def __setitem__(self, index, value):
        if self.__input[index] != value:
             self.__change_flag = True
        self.__input[index] = value


    @property
    def change_flag(self):
        return self.__change_flag
    
    @change_flag.setter
    def change_flag(self, value):
        raise RuntimeError("change flag in an internal value and can not be modified")
    

    def __get_output(self):
        if X in self:
            return X
        _input = [i for i in self if i in (L, H)]
        if not func.all_same(_input):
            return X
        if len(_input) == 0:    # all of inputs are N
            return N
        return _input[0]

    @property
    def output(self):
        self.__change_flag = False
        self.__output = self.__get_output()
        return self.__output


    def __repr__(self) -> str:
        self.__get_output()
        return f"{self.__input} => {self.__get_output()}, {self.__change_flag}"
        





def __test__wire():
    w = Wire(2)

    w[0] = L
    if(w.output != L):
        return False
    
    w[1] = H
    if(w.output != X):
        return False
    
    w[0] = N
    if(w.output != H):
        return False
    
    w[1] = X
    if(w.output) != X:
        return False
    return True
    
def __test__pmos():
    pass

def __test__nmos():
    pass



class Sim:

    def __init__(self, elements, netlist, output) -> None:
        self.elements = elements
        self.netlist = netlist
        self.output = output

        self.result = []

    def _change_flag(self):
        return any([i.change_flag for i in self.elements])

    def _step(self):
        self.netlist()
        self.output()
        if DEBUG:                                                               #DEBUG
            print(w0, w1, p0, n0, sep='\n', end="\n##########\n")               #DEBUG

    def solve(self):
        while True:
            self._step()
            if not self._change_flag():
                break

 

if __name__ == "__main__":
    input = H

    w0 = Wire()
    p0 = PMOS()
    n0 = NMOS()
    w1 = Wire(2)

    # print("initial")
    # print(w0, w1, p0, n0, sep='\n', end="\n##########\n")


    # change_flag = True
    # while change_flag:
    #     w0[0] = input
    #     w1[0] = p0.output
    #     w1[1] = n0.output

    #     p0.input = H
    #     p0.gate = w0.output

    #     n0.input = L
    #     n0.gate = w0.output

    #     def change_flag():
    #         elements = [w0, w1, p0, n0]
    #         flags = [i.change_flag for i in elements]
    #         return any(flags)

    #     print(w0, w1, p0, n0, sep='\n', end="\n##########\n")
    #     print(w1.output)
    #     print(w0, w1, p0, n0, sep='\n', end="\n##########\n")
    #     if not change_flag():
    #         break

    # def netlist():
    #     w0[0] = input
    #     w1[0] = p0.output
    #     w1[1] = n0.output

    #     p0.input = H
    #     p0.gate = w0.output

    #     n0.input = L
    #     n0.gate = w0.output

    # def output():
    #     w1.output

    # sim = Sim([w0, w1, p0, n0], netlist, output)
    # sim.solve()
    # print(w1.output)


    N = Not()
    N.input = input
    print(N.output)



    print("DONE")