
from typing import Any


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
    

class Buf:
    def __init__(self, pd = 0) -> None:
        self.input = Signal()
        self.pd = pd
        self.__output = Signal()

        self.__old_data = []
    
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
        return self.__output


    def netlist(self):
        self.__output.value = self.input.value
        self.__output.t = self.input.t + self.pd


class Not:
    def __init__(self, pd=0) -> None:
        self.input = Signal()
        self.pd = pd
        self.__output = Signal()

        self.__old_data = []

    # @property
    # def data_list(self):
    #     data


# using it interactively
# buf = Buf(pd=10)

# buf.input = Signal(value=L)
# print(buf.output)

# buf.input = Signal(value=H)
# print(buf.output)




# ---------------------
import matplotlib.pyplot as plt 
from typing import List

class Simulator:

    def __init__(self) -> None:
        self.t = 0
        self.input_pattern = None
        self.output_pattern = []
        
    def run(self, func):
        
        for pattern in self.input_pattern:
            self.output_pattern += func(pattern)

    
    def plot(self, signal: List[Signal], label=""):
        #TODO: add X and N in singnal output
        plot_time = []
        plot_value = []
        
        for index, sig in enumerate(signal):
            sig: Signal
            
            if(index > 0):
                prev_sig = signal[index-1]
                if (sig.value != prev_sig.value):
                    plot_time += [sig.t, sig.t]
                    plot_value += [prev_sig.value, sig.value]
                else:
                    plot_time += [sig.t]
                    plot_value += [sig.value]
            else:
                    plot_time += [sig.t]
                    plot_value += [sig.value]
            
        plt.plot(plot_time, plot_value, label=label)
        plt.legend()
        plt.show()

        


def input_pattern_generator():
    data = [
        Signal(t=0, value=H),
        Signal(t=10, value=L),
        Signal(t=20, value=H),
        Signal(t=30, value=H),
        Signal(t=40, value=H),
        Signal(t=50, value=H),
        Signal(t=60, value=H),
    ]
    return data

def Main(input: Signal):
    buf = Buf(pd=10)
    buf.input = input
    
    buf_out = buf.output

    return [buf_out]

sim = Simulator()
sim.input_pattern = input_pattern_generator()
sim.run(Main)

print(sim.output_pattern)
sim.plot(sim.output_pattern, "buf output")











