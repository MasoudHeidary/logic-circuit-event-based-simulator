from cgatebase import *
from cbasicgate import Wire

class NMOS(GateBase):
    def __init__(self, IN=Signal(), GATE=Signal(), tpd=0) -> None:
        super().__init__()
        self.IN = IN
        self.GATE = GATE
        self.tpd = tpd

        self.__out_buf = Signal()

    @property
    def data_list(self):
        return [self.IN, self.GATE]

    @property
    def OUT(self) -> Signal:
        self.run()
        return self.__out_buf.copy()

    def netlist(self):
        # timing
        input_t = [self.GATE.t, self.IN.t]
        self.__out_buf.t = max(input_t) + self.tpd

        # logic
        g_value = self.GATE.v
        if g_value == V.H:
            self.__out_buf.v = self.IN.v
        elif g_value == V.L:
            self.__out_buf.v = V.N
        else:
            self.__out_buf.v = self.GATE.v


class PMOS(GateBase):
    def __init__(self, IN=Signal(), GATE=Signal(), tpd=0) -> None:
        super().__init__()
        self.IN = IN
        self.GATE = GATE
        self.tpd = tpd

        self.__out_buf = Signal()

    @property
    def data_list(self):
        return [self.IN, self.GATE]
    
    @property
    def OUT(self) -> Signal:
        self.run()
        return self.__out_buf.copy()

    def netlist(self):
        #timing
        input_t = [self.GATE.t, self.IN.t]
        self.__out_buf.t = max(input_t) + self.tpd

        # logic
        g_value = self.GATE.v
        if g_value == V.L:
            self.__out_buf.v = self.IN.v
        elif g_value == V.H:
            self.__out_buf.v = V.N
        else:
            self.__out_buf.v = self.GATE.v



class Not(Gate):
    def __init__(self, IN=Signal()) -> None:
        super().__init__()
        self.IN = IN
        
        self.p = PMOS()
        self.n = NMOS()
        self.w = Wire(in_len=2)

        self.__out_buf = Signal()

    @property
    def data_list(self):
        return [self.IN]
    @property
    def element_list(self):
        return [self.p, self.n, self.w]
    
    @property
    def OUT(self) -> Signal:
        self.run()
        return self.__out_buf.copy()
    
    def netlist(self):
        self.p.IN = Signal(v=V.H)
        self.p.GATE = self.IN
        
        self.n.IN = Signal(v=V.L)
        self.n.GATE = self.IN

        self.w.IN[0] = self.n.OUT
        self.w.IN[1] = self.p.OUT
        self.__out_buf = self.w.OUT


class Transmission(Gate):
    def __init__(self, IN=False, PIn=False, NIn=False) -> None:
        super().__init__()
        self.IN = Signal() if IN==False else IN
        self.PIn = Signal() if PIn==False else PIn
        self.NIn = Signal() if NIn==False else NIn
        
        self.p = PMOS()
        self.n = NMOS()
        self.w = Wire(in_len=2)

        self.__out_buf = Signal()

    @property
    def data_list(self):
        return [self.IN, self.PIn, self.NIn]
    @property
    def element_list(self):
        return [self.p, self.n, self.w]
    
    @property
    def OUT(self):
        self.run()
        return self.__out_buf.copy()
    
    def netlist(self):
        self.p.IN = self.IN
        self.p.GATE = self.PIn

        self.n.IN = self.IN
        self.n.GATE = self.NIn

        self.w.IN[0] = self.p.OUT
        self.w.IN[1] = self.n.OUT
        self.__out_buf = self.w.OUT



##################################### TEST
def test_nmos():
    nmos = NMOS(tpd=10)

    input = [
        [Signal(V.L, 10), Signal(V.H, 0),],
        [Signal(V.L, 20), Signal(V.L, 0),],
        [Signal(V.H, 30), Signal(V.H, 0),],
        [Signal(V.H, 40), Signal(V.L, 0),],
        [Signal(V.X, 50), Signal(V.L, 0),],
        [Signal(V.L, 60), Signal(V.X, 0),],
    ]

    output = [
        Signal(V.N, 20),
        Signal(V.N, 30),
        Signal(V.H, 40),
        Signal(V.L, 50),
        Signal(V.X, 60),
        Signal(V.N, 70),
    ]

    for in_index, in_value in enumerate(input):
        nmos.GATE = in_value[0]
        nmos.IN = in_value[1]
        
        out = nmos.OUT
        xout = output[in_index]
        if out != xout:
            print(f"{in_value} \t=> NMOS =>\t {out} (expected: {xout}) [FALSE]")
            return False
        else:
            print(f"{in_value} \t=> NMOS =>\t {out} \t[TRUE]")
    return True


def test_not():
    g_not = Not()

    input = [
        Signal(V.X, 0),
        Signal(V.N, 0),
        Signal(V.L, 0),
        Signal(V.H, 0),
    ]

    output = [
        Signal(V.X, 0),
        Signal(V.N, 0),
        Signal(V.H, 0),
        Signal(V.L, 0),
    ]

    for in_index, in_value in enumerate(input):
        g_not.IN = in_value
        
        out = g_not.OUT
        xout = output[in_index]
        if out != xout:
            print(f"{in_value} \t=> NOT =>\t {out} (expected: {xout}) [FALSE]")
            return False
        else:
            print(f"{in_value} \t=> NOT =>\t {out} \t[TRUE]")
    return True


if __name__ == "__main__":
    test_list = [
        ('NMOS', test_nmos),
        ('NOT', test_not),
    ]

    print("RUNNING TEST")
    for name, func in test_list:
        print(f"{name} \t[{func()}]")
##################################### END TEST