from typing import List
import matplotlib.pyplot as plt 

from csig import *


class Plot:
    def __init__(self) -> None:
        pass

    def __t_range(self, lst_signal: List[List[Signal]]):
        _t = []
        for _lst_sig in lst_signal:
            _t += [i.t for i in _lst_sig]

        return sorted(list(set(_t)))
    

    def __sampling(self, time: List[int], signal: List[Signal]):
        _ret: List[Signal] = []
        
        _sig_index = 0
        _sig_len = len(signal)
        for t in time:
            v = None

            for i in range(_sig_index, _sig_len):
                if signal[i].t > t:
                    break
                _sig_index = i
                v = signal[i].v

            _ret.append(Signal(v=v, t=t))
        
        return _ret
    

    # NOTE: this will make signal abnormal and not usuable but good to plot
    def __square_signal(self, signal: List[Signal]):
        _ret: List[Signal] = []

        for index, sig in enumerate(signal):
            
            if index > 0:
                prev_sig = signal[index-1]
                if(sig.v != prev_sig.v):
                    _ret += [
                        Signal(v=prev_sig.v, t=sig.t), 
                        Signal(v=sig.v, t=sig.t)
                        ]
                else:
                    _ret += [
                        Signal(v=sig.v, t=sig.t)
                        ]
            else:
                _ret += [
                    Signal(v=sig.v, t=sig.t)
                    ]

            
            # TODO: define X and N values


        return _ret

    def __pre_process(self, lst_signal: List[List[Signal]]):
        time_range = self.__t_range(lst_signal)

        _data: List[Signal] = []
        for signal in lst_signal:
            _data += [
                self.__square_signal(
                    self.__sampling(time_range, signal)
                )
            ]
        return _data

    def plot(self, **kwargs):
        len_signals = len(kwargs['signal'])

        
        plot_data = self.__pre_process(
            kwargs['signal']
        )

        for col in range(len_signals):
            plt.subplot(len_signals, 1, col+1)
            plt.plot(
                [s.t for s in plot_data[col]],
                [s.v for s in plot_data[col]],
                # label = kwargs.get('label') or "",
                linewidth = kwargs.get('linewidth') or 2.5
            )
            try:
                plt.title(kwargs.get('label')[col])
            except:
                pass # no title for the plot

        plt.legend()
        plt.show()
            


# class DynamicSimulator:

#     def __init__(self, sig: Signal = False, sig_list: List[Signal] = False) -> None:
#         self.sig = sig
#         self.sig_list = sig_list

#         self.data = []

#     def save(self, input: Signal = False, input_list: List[Signal] = False):
#         if input or input_list:
#             if (self.sig or self.sig_list) != False:
#                 raise RuntimeError("this simulator is saving input, create another simulator")
#             self.data += [input.copy()]
#         elif self.sig:
#             self.data += [self.sig].copy()
#         elif self.sig_list:
#             self.data += self.sig_list.copy()
#         else:
#             raise RuntimeError("no data to save!")
        
#     def get_data(self):
#         return self.data


# class DynamicSimulator:

#     def __init__(self):
#         self.data = []

#     def get_data(self):
#         return self.data

#     def run(self, func, **kwargs):
#         for values in zip(kwargs.values()):
#             for i in values:
#                 func()


    


# class Simulator:

#     def __init__(self) -> None:
#         pass

#     def run(self, func, **kwargs):
#         self.output_buf = []
#         for pattern in 

# class Simulator:

#     def __init__(self) -> None:
#         self.t = 0
        
#     def run(self, func, input):
#         self.output_buf = []
#         for pattern in input:
#             self.output_buf += func(pattern)
#         return self.output_buf


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










