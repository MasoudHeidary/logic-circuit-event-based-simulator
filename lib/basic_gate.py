

L = 0
H = 1
N = 2
X = 3

class Signal:
    def __init__(self, t = 0, value = X) -> None:
        self.t = t
        self.value = value

    def __eq__(self, obj) -> bool:
        if ((self.t == obj.t) and (self.value == obj.value)):
            return True
        return False
    
    def __repr__(self) -> str:
        return str({'t': self.t, 'value': self.value})
    
    def copy(self) -> object:
        return Signal(self.t, self.value)
    


class GateBase:

    def __init__(self) -> None:
        self.input = Signal()
        self.output_buf = Signal()
        self.__old_data = None

    @property
    def data_list(self):
        data = [
            self.input,
        ]
        return data

    @property
    def change_flag(self):
        data = self.data_list
        if (data == self.__old_data):
            return False
        self.__old_data = data
        return True

    @property
    def output(self):
        while self.change_flag:
            self.netlist()
        return self.output_buf.copy()
    
    def netlist(self):
        pass




class Buf(GateBase):
    def __init__(self, pd=0) -> None:
        super().__init__()
        self.pd = pd

    def netlist(self):
        self.output_buf.value = self.input.value
        self.output_buf.t = self.input.t + self.pd


class Not(GateBase):
    def __init__(self, pd=0) -> None:
        super().__init__()
        self.pd = pd
    
    def netlist(self):
        # logic
        if self.input.value in [L, H]:
            self.output_buf.value = not self.input.value
        else:
            self.output_buf.value = self.input.value

        # timing
        self.output_buf.t = self.input.t + self.pd