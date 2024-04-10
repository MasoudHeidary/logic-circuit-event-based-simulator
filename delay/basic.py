import func




class Signal:
    L = 0
    H = 1
    X = 2
    N = 3
    
    def __init__(self, v = N, t = 0) -> None:
        self.v = v
        self.t = t

    def __repr__(self) -> str:
        return str({'v': self.v, 't': self.t})
    
    def __eq__(self, other: object) -> bool:
        if(self.v == other.v):
            return True
        return False

class NMOS:
    def __init__(self, t = 0) -> None:
        self.input = Signal()
        self.gate = Signal()
        self.t = t

        self.__old_data = []
        self.__output = Signal()

    @property
    def data_list(self):
        data = [
            self.input.v,
            self.gate.v,
            self.t
        ]
        return data

    @property
    def change_flag(self):
        data = self.data_list
        if data != self.__old_data:
            self.__old_data = data
            return True
        return False


    @property
    def output(self) -> Signal:
        while self.change_flag:
            self.netlist()
        return self.__output

    
    # TODO: add description
    def netlist(self):
        
        # voltage
        if(Signal.X in [self.gate.v, self.input.v]):
            self.__output.v = Signal.X
        elif(self.gate.v == Signal.H):
            self.__output.v = self.input.v
        else:
            self.__output.v = Signal.N
        
        # delay
        self.__output.t = max(self.gate.t, self.input.t) + self.t

    # TODO: add test


    


def __test_NMOS():
    pass

    n = NMOS()
    n.input = Signal(Signal.L)
    n.gate = Signal(Signal.L)

    if(n.output.v != Signal.N):
        return False
    
    n.gate.v = Signal.H
    if(n.output.v != Signal.L):
        return False
    
    n = NMOS(t=1)
    n.input = Signal(Signal.H, 3)
    n.gate = Signal(Signal.H)
    if(n.output.t != 4):
        return False
    
    return True

print(__test_NMOS())




class PMOS:
    def __init__(self, t=0) -> None:
        self.input = Signal()
        self.gate = Signal()
        self.t = t

        self.__old_data = []
        self.__output = Signal()

    
    @property
    def data_list(self):
        data = [
            self.input.v,
            self.gate.v,
            self.t
        ]
        return data
    
    @property
    def change_flag(self):
        data = self.data_list
        if data != self.__old_data:
            self.__old_data = data
            return True
        return False
    
    @property
    def output(self) -> Signal:
        while self.change_flag:
            self.netlist()
        return self.__output
    

    def netlist(self):

        # voltage
        if(Signal.X in [self.gate.v, self.input.v]):
            self.__output.v = Signal.X
        elif (self.gate.v == Signal.L):
            self.__output.v = self.input.v
        else:
            self.__output.v = Signal.N

        # delay
        self.__output.t = max(self.gate.t, self.input.t) + self.t


    # TODO: add test
    def __test__(self):
         self.gate.v = Signal.H
         self.input.v = Signal.H
         if(self.output.v != Signal.N):
             return False
         
         self.gate.v = Signal.L
         self.input.v = Signal.H
         if(self.output.v != Signal.H):
             return False
         
         self.t = 1
         self.gate.t = 2
         self.input.t = 3
         if(self.output.t != 4):
             return False

         return True
         
         
print(PMOS().__test__())




class Wire:
    def __init__(self, in_len=1, t=0) -> None:
        self.input = [Signal() for _ in range(in_len)]
        self.t = t

        self.__old_data = []
        self.__output = Signal()

    @property 
    def data_list(self):
        data = self.input + [self.t]
        return data
    
    @property
    def change_flag(self):
        data = self.data_list
        if data != self.__old_data:
            self.__old_data = data
            return True
        return False
    
    @property
    def output(self) -> Signal:
        while self.change_flag:
            self.netlist()
        return self.__output
    

    def netlist(self):
        
        # voltage
        _input = [i.v for i in self.input if i.v in (Signal.L, Signal.H)]
        
        if(Signal.X in [_.v for _ in self.input]):
            self.__output.v = Signal.X
        elif not func.all_same(_input):
            self.__output.v = Signal.X
        elif(len(_input) == 0):
            self.__output = Signal.N
        else:
            self.__output = _input[0]

