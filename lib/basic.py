from typing import List
import matplotlib.pyplot as plt 

from csig import *


# class Pattern:
#     def __init__(self) -> None:
#         self.t = 0
#         self.v = X

#         self.__pattern = []

#     def get_data(self):
#         return self.__pattern


#     def delay(self, t):
#         self.__pattern += [Signal(t=self.t, value=self.v)]
#         self.t += t
    


class Simulator:

    def __init__(self) -> None:
        self.t = 0
        
    def run(self, func, input):
        self.output_buf = []
        for pattern in input:
            self.output_buf += func(pattern)
        return self.output_buf

    
    def __plot_data_process(self, signal: List[Signal]):
        #TODO: add X and N in singnal output
        plot_time = []
        plot_value = []
        

        # fill signal from 0 to initial value
        zero_sig = signal[0]
        if zero_sig.t != 0:
            signal.insert(0, Signal(t=0, value=X))

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

        # place X as 0.5 in value
        for index, pv in enumerate(plot_value):
            if pv in [X, N]:
                plot_value[index] = 0.5

        return (plot_time, plot_value)


    # def plot(self, signal: List[Signal], label=""):
        
    #     plot_data = self.__plot_data_process(signal)
            
    #     plt.plot(plot_data[0], plot_data[1], label=label, linewidth=2.5)
    #     plt.legend()
    #     plt.show()

    def plot(self, *args, **kwargs):
        number_of_signals = len(kwargs['signal'])

        for col in range(number_of_signals):
            plot_data = self.__plot_data_process(
                kwargs['signal'][col]
            )

            plt.subplot(number_of_signals, 1, col + 1)
            plt.plot(
                plot_data[0], 
                plot_data[1], 
                label=kwargs.get('label') or "",
                linewidth=kwargs.get("linewidth") or 2.5
            )
        
        plt.legend()
        plt.show()

    

        


# def input_pattern_generator():
#     data = [
#         Signal(t=0, value=H),
#         Signal(t=10, value=L),
#         Signal(t=20, value=H),
#         Signal(t=30, value=H),
#         Signal(t=40, value=H),
#         Signal(t=50, value=H),
#         Signal(t=60, value=H),
#     ]
#     return data

# def Main(input: Signal):
#     buf = Buf(pd=10)
#     buf.input = input
    
#     buf_out = buf.output

#     return [buf_out]

# sim = Simulator()
# sim.input_pattern = input_pattern_generator()
# sim.run(Main)

# print(sim.output_pattern)
# sim.plot(sim.output_pattern, "buf output")










