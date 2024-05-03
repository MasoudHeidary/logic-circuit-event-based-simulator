from cgatebase import *

class Buf(GateBase):
    def __init__(self, IN=Signal(), tpd=0) -> None:
        super().__init__()
        
        self.IN = IN
        self.tpd = tpd
        self.__out_buf = Signal()

    @property
    def data_list(self):
        return [self.IN, self.tpd]

    @property
    def OUT(self):
        self.run()
        return self.__out_buf.copy()

    def netlist(self):
        self.__out_buf.t = self.IN.t + self.tpd     # timing
        self.__out_buf.v = self.IN.v        # logic



class Wire(GateBase):
    def __init__(self, IN=False, in_len=1, tpd=0) -> None:
        super().__init__()
        self.IN = [Signal() for _ in range(in_len)] if IN==False else IN
        self.tpd = tpd

        self.__out_buf = Signal()

    @property
    def data_list(self):
        return self.IN + [self.tpd]
    

    @property
    def OUT(self):
        self.run()
        return self.__out_buf.copy()
    
    def netlist(self):
        #timing

        # logic
        input_v = [i.v for i in self.IN]
        valid_input_v = V.get_valid(input_v)
        if V.X in input_v:
            self.__out_buf.v = V.X
        elif not V.all_same(valid_input_v):
            self.__out_buf.v = V.X
        elif len(valid_input_v) == 0:
            self.__out_buf.v = V.N
        else:
            self.__out_buf.v = valid_input_v[0]

        



# class Not(GateBase):
#     def __init__(self, pd=0) -> None:
#         super().__init__()
#         self.pd = pd
    
#     def netlist(self):
#         # logic
#         if self.input.value in V.valid:
#             self.output_buf.value = not self.input.value
#         else:
#             self.output_buf.value = self.input.value

#         # timing
#         self.output_buf.t = self.input.t + self.pd


# class Wire(SemiComplexGateBase):
#     def __init__(self, in_len=2, out_len=1) -> None:
#         super().__init__(in_len, out_len)
    
#     def netlist(self):
#         # timing
#         input_time = [i.t for i in self.input]
#         self.output_buf.t = max(input_time) + self.pd

#         # logic
#         input_value = [i.value for i in self.input]
#         if V.X in input_value:
#             self.output_buf.value = V.X
        
#         pure_input_value = [i for i in input_value if i in V.valid]
#         if(len(pure_input_value) == 0):
#             self.output_buf.value = V.N
        
#         def all_same(lst):
#             return all(elem==lst[0] for elem in lst)
#         if not all_same(pure_input_value):
#             self.output_buf.value = V.N
#         self.output_buf.value = self.input[0].value
        


# class And(SemiComplexGateBase):
#     def __init__(self, input=False, in_len=2, pd=0) -> None:
#         super().__init__(input, in_len)
#         self.pd = pd

#     def netlist(self):
#         # timing
#         self.output_buf.t = max([i.t for i in self.input]) + self.pd

#         # logic
#         input_value = [i.value for i in self.input]
#         self.output_buf.value = V.all(input_value)

class And(GateBase):
    def __init__(self, IN=False, in_len=2, tpd=0) -> None:
        super().__init__()
        self.IN = [Signal() for _ in range(in_len)] if IN==False else IN
        self.tpd = tpd

        self.__out_buf = Signal()

    @property
    def data_list(self):
        return self.IN
    
    @property
    def OUT(self):
        self.run()
        return self.__out_buf
    
    def netlist(self):
        input_time = [i.t for i in self.IN]
        self.__out_buf.t = max(input_time) + self.tpd
        
        input_value = [i.v for i in self.IN]
        self.__out_buf.v = V.all(input_value)




################################# TEST
def test_buf():
    buf = Buf(tpd=10)
    
    input = [
        Signal(V.L, 0),
        Signal(V.H, 10),
        Signal(V.H, 20),
        Signal(V.L, 30),
        Signal(V.X, 40),
        Signal(V.N, 50),
    ]
    output = [
        Signal(V.L, 10),
        Signal(V.H, 20),
        Signal(V.H, 30),
        Signal(V.L, 40),
        Signal(V.X, 50),
        Signal(V.N, 60),
    ]

    for in_index, in_value in enumerate(input):
        buf.IN = in_value
        if buf.OUT != output[in_index]:
            print(f"{in_value} \t=> BUF =>\t {buf.OUT} (expected: {output[in_index]}) [FALSE]")
            return False
        else:
            print(f"{in_value} \t=> BUF =>\t {buf.OUT} \t[TRUE]")
    return True


def test_and():
    gand = And(tpd=10)

    input = [
        (Signal(V.L, 0), Signal(V.L, 10)),
        (Signal(V.L, 0), Signal(V.H, 20)),
        (Signal(V.H, 0), Signal(V.H, 30)),
        (Signal(V.H, 0), Signal(V.L, 40)),
        (Signal(V.X, 0), Signal(V.H, 50)),
        (Signal(V.N, 0), Signal(V.H, 60)),
    ]
    output = [
        Signal(V.L, 20),
        Signal(V.L, 30),
        Signal(V.H, 40),
        Signal(V.L, 50),
        Signal(V.X, 60),
        Signal(V.H, 70),
    ]

    for in_index, in_value in enumerate(input):
        gand.IN[0] = in_value[0]
        gand.IN[1] = in_value[1]
        if gand.OUT != output[in_index]:
            print(f"{in_value[0]}, {in_value[1]} \t=> AND =>\t {gand.OUT} (expected: {output[in_index]}) [FALSE]")
            return False
        else:
            print(f"{in_value[0]}, {in_value[1]} \t=> AND =>\t {gand.OUT} \t[TRUE]")
    return True


if __name__ == "__main__":
    test_list = [
        ('BUFFER', test_buf),
        ('AND', test_and),
    ]

    print("RUNNING TEST")
    for name, func in test_list:
        print(f"{name} \t[{func()}]")
    # t 
################################# END TEST


 