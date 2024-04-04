from sim import *

class Not:

    def __init__(self) -> None:
        self._input = N
        self._output = N

        self.win = Wire()
        self.p = PMOS()
        self.n = NMOS()
        self.wout = Wire(2)
        self.elements = [self.win, self.p, self.n, self.wout]

    def netlist(self):
        self.win[0] = self.input
        self.p.input = H
        self.p.gate = self.win.output
        self.n.input = L
        self.n.gate = self.win.output
        self.wout[0] = self.p.output
        self.wout[1] = self.n.output
        self.output = self.wout.output

    @property
    def change_flag(self):
        return any([i.change_flag for i in self.elements])

    # input pins
    @property
    def input(self):
        return self._input
    
    @input.setter
    def input(self, value):
        self._input = value

    @property
    def output(self):
        self.netlist()
        while self.change_flag:
            self.netlist()
        return self._output
    
    @output.setter
    def output(self, value):
        self._output = value

    def __repr__(self) -> str:
        return f"{self.input} -> {self.output}"


class And:

    def __init__(self) -> None:
        self.A = N
        self.B = N
        self.__output = N

        self.p = [PMOS() for _ in range(2)]
        self.n = [NMOS() for _ in range(2)]
        self.w = Wire(3)
        self.ngate = Not()

        self.elements = self.p + self.n + [self.w, self.ngate]

    def netlist(self):

        self.p[0].input = H
        self.p[0].gate = self.A
        self.w[0] = self.p[0].output

        self.p[1].input = H
        self.p[1].gate = self.B
        self.w[1] = self.p[1].output

        self.w[2] = self.n[0].output
        self.n[0].gate = self.A
        self.n[0].input = self.n[1].output

        self.n[1].gate = self.B
        self.n[1].input = L

        self.ngate.input = self.w.output
        self.__output = self.ngate.output
        
    @property
    def change_flag(self):
        return any([i.change_flag for i in self.elements])

    @property
    def output(self):
        self.netlist()
        while self.change_flag:
            self.netlist()
        return self.__output


def __test__and():
    g_and = And()

    g_and.A = L
    g_and.B = L
    if (g_and.output != L):
        raise RuntimeError()
    print(g_and.output)

    g_and.A = H
    if (g_and.output != L):
        raise RuntimeError()
    print(g_and.output)

    g_and.B = H
    if(g_and.output != H):
        raise RuntimeError()
    print(g_and.output)

    print(g_and.n[0].gate)


if __name__ == "__main__":
    __test__and()



