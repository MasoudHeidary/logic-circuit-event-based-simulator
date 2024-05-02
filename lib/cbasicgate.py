from cgatebase import *

class Buf(GateBase):
    def __init__(self, pd=0) -> None:
        super().__init__()
        self.pd = pd

    def netlist(self):
        self.output_buf.value = self.input.value
        self.output_buf.t = self.input.t + self.pd


def test_buf():
    buf = Buf(10)
    
    input = [
        Signal(V.L, 0),
        Signal(V.H, 10),
        Signal(V.H, 20),
        Signal(V.L, 30)
    ]
    output = [
        Signal(V.L, 10),
        Signal(V.H, 20),
        Signal(V.H, 30),
        Signal(V.L, 40),
    ]

    for in_index, in_value in enumerate(input):
        buf.input = in_value
        if buf.output != output[in_index]:
            print(f"{in_value} => BUF => {buf.output} (expected: {output[in_index]}) [FALSE]")
            return False
        else:
            print(f"{in_value} => BUF => {buf.output} [TRUE]")
    return True



class Not(GateBase):
    def __init__(self, pd=0) -> None:
        super().__init__()
        self.pd = pd
    
    def netlist(self):
        # logic
        if self.input.value in V.valid:
            self.output_buf.value = not self.input.value
        else:
            self.output_buf.value = self.input.value

        # timing
        self.output_buf.t = self.input.t + self.pd


class Wire(SemiComplexGateBase):
    def __init__(self, in_len=2, out_len=1) -> None:
        super().__init__(in_len, out_len)
    
    def netlist(self):
        # timing
        input_time = [i.t for i in self.input]
        self.output_buf.t = max(input_time) + self.pd

        # logic
        input_value = [i.value for i in self.input]
        if V.X in input_value:
            self.output_buf.value = V.X
        
        pure_input_value = [i for i in input_value if i in V.valid]
        if(len(pure_input_value) == 0):
            self.output_buf.value = V.N
        
        def all_same(lst):
            return all(elem==lst[0] for elem in lst)
        if not all_same(pure_input_value):
            self.output_buf.value = V.N
        self.output_buf.value = self.input[0].value
        


class And(SemiComplexGateBase):
    def __init__(self, input=False, in_len=2, pd=0) -> None:
        super().__init__(input, in_len)
        self.pd = pd

    def netlist(self):
        # timing
        self.output_buf.t = max([i.t for i in self.input]) + self.pd

        # logic
        input_value = [i.value for i in self.input]
        self.output_buf.value = V.all(input_value)


def test_and():
    A = Signal(V.H, 0)
    B = [
        Signal(V.L, 0),
        Signal(V.H, 10),
        Signal(V.H, 20),
        Signal(V.L, 30)
    ]

    output = [
        Signal(V.L, 10),
        Signal(V.H, 20),
        Signal(V.H, 30),
        Signal(V.L, 40),
    ]

    for B_index, B_value in enumerate(B):
        gand = And(input=[A, B_value],in_len=2, pd=10)
        if gand.output != output[B_index]:
            print(f"{A}, {B_value} => AND => {gand.output} (expected: {output[B_index]}) [FALSE]")
            return False
        else:
            print(f"{A}, {B_value} => AND => {gand.output} [TRUE]")
    return True


if __name__ == "__main__":
    test_buf()
    test_and()