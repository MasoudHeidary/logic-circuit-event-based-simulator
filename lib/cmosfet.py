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

# BUG: if don't use a gate which is added, change_flag will stay True
class And(Gate):
    def __init__(self, IN=False, in_len=2) -> None:
        super().__init__()
        self.in_len = in_len
        self.IN = [Signal() for _ in range(in_len)] if IN==False else IN

        self.p = [PMOS() for _ in range(in_len)]
        self.n = [NMOS() for _ in range(in_len)]
        self.gnot = Not()
        self.w = Wire(in_len= in_len+1)

        self.__out = Signal()

    @property
    def data_list(self):
        return self.IN
    @property
    def element_list(self):
        return [self.gnot, self.w] + self.p + self.n
    
    @property
    def OUT(self) -> Signal:
        self.run()
        return self.__out.copy()
    
    def netlist(self):
        for i in range(self.in_len):
            self.p[i].IN = Signal(v=V.H)
            self.p[i].GATE = self.IN[i]
            self.w.IN[i] = self.p[i].OUT

            self.n[i].GATE = self.IN[i]
            self.n[i].IN = Signal(v=V.L) if i==self.in_len-1 else self.n[i+1].OUT

        self.w.IN[self.in_len] = self.n[0].OUT    
        self.gnot.IN = self.w.OUT
        self.__out = self.gnot.OUT

    

class Transmission(Gate):
    def __init__(self, IN=Signal(), PIn=Signal(), NIn=Signal()) -> None:
        super().__init__()
        self.IN = IN
        self.PIn = PIn
        self.NIn = NIn
        
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

class FA(Gate):
    def __init__(self, A=Signal(), B=Signal(), C=Signal()) -> None:
        super().__init__()
        self.A = A
        self.B = B
        self.C = C

        self.g_not_a = Not()
        self.g_not_b = Not()
        self.g_not_c = Not()

        self.g_not_xx = Not()
        self.g_tra_xx = [Transmission() for _ in range(2)]
        self.w_xx = Wire(in_len=2)

        self.g_tra_sum = [Transmission() for _ in range(2)]
        self.w_sum = Wire(in_len=2)
        self.g_tra_carry = [Transmission() for _ in range(2)]
        self.w_carry = Wire(in_len=2)
    
        self.__sum = Signal()
        self.__carry = Signal()

    @property
    def data_list(self):
        return [self.A, self.B, self.C]
    @property
    def element_list(self):
        _data = [
            self.g_not_a, self.g_not_b, self.g_not_c, self.g_not_xx,
            self.w_xx, self.w_sum, self.w_carry,
        ] \
        + self.g_tra_xx \
        + self.g_tra_sum \
        + self.g_tra_carry
        return _data
    

    @property
    def sum(self):
        self.run()
        return self.__sum.copy()
    @property
    def carry(self):
        self.run()
        return self.__carry.copy()
    
    def netlist(self):
        self.g_not_a.IN = self.A
        self.g_not_b.IN = self.B
        self.g_not_c.IN = self.C

        # not of inputs
        self.nA = self.g_not_a.OUT
        self.nB =  self.g_not_b.OUT
        self.nC = self.g_not_c.OUT

        # xx
        self.g_tra_xx[0].IN = self.A
        self.g_tra_xx[0].PIn = self.B
        self.g_tra_xx[0].NIn = self.nB
        self.w_xx.IN[0] = self.g_tra_xx[0].OUT
        self.g_tra_xx[1].IN = self.nA
        self.g_tra_xx[1].PIn = self.nB
        self.g_tra_xx[1].NIn = self.B
        self.w_xx.IN[1] = self.g_tra_xx[1].OUT
        self.xx = self.w_xx.OUT

        # nxx
        self.g_not_xx.IN = self.xx
        self.nxx = self.g_not_xx.OUT

        # sum
        self.g_tra_sum[0].IN = self.C
        self.g_tra_sum[0].PIn = self.xx
        self.g_tra_sum[0].NIn = self.nxx
        self.w_sum.IN[0] = self.g_tra_sum[0].OUT
        self.g_tra_sum[1].IN = self.nC
        self.g_tra_sum[1].PIn = self.nxx
        self.g_tra_sum[1].NIn = self.xx
        self.w_sum.IN[1] = self.g_tra_sum[1].OUT
        self.__sum = self.w_sum.OUT

        # carry
        self.g_tra_carry[0].IN = self.C
        self.g_tra_carry[0].PIn = self.nxx
        self.g_tra_carry[0].NIn = self.xx
        self.w_carry.IN[0] = self.g_tra_carry[0].OUT
        self.g_tra_carry[1].IN = self.A
        self.g_tra_carry[1].PIn = self.xx
        self.g_tra_carry[1].NIn = self.nxx
        self.w_carry.IN[1] = self.g_tra_carry[1].OUT
        self.__carry = self.w_carry.OUT




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


def test_and():
    g_and = And(in_len=3)

    input = [
        [Signal(v=V.L), Signal(v=V.L), Signal(v=V.L),],
        [Signal(v=V.L), Signal(v=V.L), Signal(v=V.H),],
        [Signal(v=V.L), Signal(v=V.H), Signal(v=V.L),],
        [Signal(v=V.L), Signal(v=V.H), Signal(v=V.H),],
        [Signal(v=V.H), Signal(v=V.L), Signal(v=V.L),],
        [Signal(v=V.H), Signal(v=V.L), Signal(v=V.H),],
        [Signal(v=V.H), Signal(v=V.H), Signal(v=V.L),],
        [Signal(v=V.H), Signal(v=V.H), Signal(v=V.H),],
    ]

    output = [
        Signal(v=V.L),
        Signal(v=V.L),
        Signal(v=V.L),
        Signal(v=V.L),
        Signal(v=V.L),
        Signal(v=V.L),
        Signal(v=V.L),
        Signal(v=V.H),
    ]

    for in_index, in_value in enumerate(input):
        g_and.IN = in_value
        
        out = g_and.OUT
        xout = output[in_index]
        if out != xout:
            print(f"{in_value} \t=> AND =>\t {out} (expected: {xout}) [FALSE]")
            return False
        else:
            print(f"{in_value} \t=> AND =>\t {out} \t[TRUE]")
    return True

def test_FA():
    g_FA = FA()

    input = [
        [Signal(V.L), Signal(V.L), Signal(V.L)],
        [Signal(V.L), Signal(V.L), Signal(V.H)],
        [Signal(V.L), Signal(V.H), Signal(V.L)],
        [Signal(V.L), Signal(V.H), Signal(V.H)],
        [Signal(V.H), Signal(V.L), Signal(V.L)],
        [Signal(V.H), Signal(V.L), Signal(V.H)],
        [Signal(V.H), Signal(V.H), Signal(V.L)],
        [Signal(V.H), Signal(V.H), Signal(V.H)],
    ]
    output = [
        [Signal(V.L), Signal(V.L)],
        [Signal(V.L), Signal(V.H)],
        [Signal(V.L), Signal(V.H)],
        [Signal(V.H), Signal(V.L)],
        [Signal(V.L), Signal(V.H)],
        [Signal(V.H), Signal(V.L)],
        [Signal(V.H), Signal(V.L)],
        [Signal(V.H), Signal(V.H)],
    ]

    for in_index, in_value in enumerate(input):
        g_FA.A = in_value[0]
        g_FA.B = in_value[1]
        g_FA.C = in_value[2]
        
        sum = g_FA.sum
        carry = g_FA.carry
        out = [carry, sum]
        xout = output[in_index]
        if out != xout:
            print(f"{in_value} \t=> FA =>\t {out} (expected: {xout}) [FALSE]")
            return False
        else:
            print(f"{in_value} \t=> FA =>\t {out} \t[TRUE]")
    return True

if __name__ == "__main__":
    test_list = [
        ('NMOS', test_nmos),
        ('NOT', test_not),
        ('AND', test_and),
        ('FA', test_FA)
    ]

    print("RUNNING TEST")
    for name, func in test_list:
        print(f"{name} \t[{func()}]")
##################################### END TEST