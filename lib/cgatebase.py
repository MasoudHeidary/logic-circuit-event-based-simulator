from csig import *


# single input, single output
class GateBase:

    def __init__(self) -> None:
        self.input = input
        self.pd = 0
        self.output_buf = Signal()
        
        self.__old_data = None

    @property
    def data_list(self):
        data = [
            self.input,
            self.pd
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


#  multi input, signle output
class SemiComplexGateBase(GateBase):
    def __init__(self, in_len=2) -> None:
        super().__init__()
        self.input = [Signal() for _ in  range(in_len)]
        # NO CHANGE in output (a single output)
        # NO CHANGE in data_list to watch

    


# multi input, multi output
class ComplexGateBase(SemiComplexGateBase):
    def __init__(self, in_len = 2, out_len = 1) -> None:
        super().__init__(in_len=in_len)
        self.output_buf = [Signal() for _ in range(out_len)]
        # NO CHANGE in data_list to watch


