from cgatebase import *


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
    def OUT(self):
        self.run()
        return self.__out_buf.copy()

    def netlist(self):
        # timing
        input_t = [self.GATE.t, self.IN.t]
        self.__out_buf.t = max(input_t) + self.tpd

        # logic
        g_value = self.GATE.value
        if g_value == V.H:
            self.__out_buf.value = self.IN.value
        elif g_value == V.L:
            self.__out_buf.value = V.N
        else:
            self.__out_buf.value = self.GATE.value


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
    def OUT(self):
        self.run()
        return self.__out_buf.copy()

    def netlist(self):
        #timing
        input_t = [self.GATE.t, self.IN.t]
        self.__out_buf.t = max(input_t) + self.tpd

        # logic
        g_value = self.GATE.value
        if g_value == V.L:
            self.__out_buf.value = self.IN.value
        elif g_value == V.H:
            self.__out_buf.value = V.N
        else:
            self.__out_buf.value = self.GATE.value






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



if __name__ == "__main__":
    test_list = [
        ('NMOS', test_nmos),
    ]

    print("RUNNING TEST")
    for name, func in test_list:
        print(f"{name} \t[{func()}]")
##################################### END TEST