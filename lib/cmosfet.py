from cgatebase import *


class NMOS(SemiComplexGateBase):
    def __init__(self, input=Signal(), gate=Signal(), pd=0) -> None:
        self.input = input
        self.gate = gate
        super().__init__([self.input, self.gate], in_len=2)
        self.pd = pd

    def netlist(self):
        # timing
        gate_t = self.gate.t
        input_t = self.input.t
        self.output_buf.t = max(gate_t, input_t) + self.pd

        # logic
        g_value = self.gate.value
        if g_value == V.H:
            self.output_buf.value = self.input.value
        else:
            self.output_buf.value = V.N


class PMOS(SemiComplexGateBase):
    def __init__(self, input=Signal(), gate=Signal(), pd=0) -> None:
        super().__init__([input, gate], in_len=2)
        self.input = input
        self.gate = gate
        self.pd = pd

    def netlist(self):
        #timing
        gate_t = self.gate.t
        input_t = self.input.t
        self.output_buf.t = max(gate_t, input_t) + self.pd

        # logic
        g_value = self.gate.value
        if g_value == V.L:
            self.output_buf.value = self.input.value
        else:
            self.output_buf.value = V.N






x = NMOS()
d = DSignal()

x.input = d.L
x.gate = d.H
print(x.output)

x.gate = d.L
print(x.output)