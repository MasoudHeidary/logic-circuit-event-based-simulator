from sim import *
from logic import *

class Trans():

    def __init__(self) -> None:
        self.ctop = N
        self.cmid = N
        self.itop = N
        self.ilow = N

        self.__output = N

        self.p0 = PMOS()
        self.n0 = NMOS()
        self.p1 = PMOS()
        self.n1 = NMOS()
        self.wo = Wire(4)
        self.elements = [self.p0, self.n0, self.p1, self.n1, self.wo]

    def netlist(self):
        self.p0.gate = self.ctop
        self.p0.input = self.itop
        self.wo[0] = self.p0.output

        self.n0.gate = self.cmid
        self.n0.input = self.itop
        self.wo[1] = self.n0.output

        self.p1.gate = self.cmid
        self.p1.input = self.ilow
        self.wo[2] = self.p1.output

        self.n1.gate = self.ctop
        self.n1.input = self.ilow
        self.wo[3] = self.n1.output

        self.__output = self.wo.output

    @property
    def change_flag(self):
        return any([i.change_flag for i in self.elements])

    @property
    def output(self):
        self.netlist()
        while self.change_flag:
            self.netlist()
        return self.__output


    

class FA:

    def __init__(self) -> None:
        self.A = N
        self.B = N
        self.C = N

        self.__sum = N
        self.__carry = N

        self.ngate = [Not() for _ in range(4)]
        self.tgate = [Trans() for _ in range(3)]
        self.elements = self.ngate + self.tgate

    def netlist(self):

        # not A B C
        self.ngate[0].input = self.A     #nA
        nA = self.ngate[0].output
        self.ngate[1].input = self.B     #nB
        nB = self.ngate[1].output
        self.ngate[2].input = self.C     #nC
        nC = self.ngate[2].output


        # generate xx signal
        self.tgate[0].ctop = self.B
        self.tgate[0].cmid = nB
        self.tgate[0].itop = self.A
        self.tgate[0].ilow = nA
        xx = self.tgate[0].output
        self.xx = xx

        # generate nxx signal
        self.ngate[3].input = self.tgate[0].output
        nxx = self.ngate[3].output

        # # generate dxx
        # self.ngate[4].input = self.tgate[0].output
        # self.ngate[5].input = self.ngate[4].output


        # generate sum
        # self.ngate[6].input = self.ngate[2].output
        # self.ngate[7].input = self.ngate[6].output
        # self.ngate[8].input = self.ngate[7].output

        # self.ngate[9].input = self.ngate[2].output
        # self.ngate[10].input = self.ngate[9].output

        self.tgate[1].ctop = xx
        self.tgate[1].cmid = nxx
        self.tgate[1].itop = self.C
        self.tgate[1].ilow = nC
        self.__sum = self.tgate[1].output


        # generate carry 
        # self.ngate[11].input = self.A
        # self.ngate[12].input = self.ngate[11].output
        # self.ngate[13].input = self.ngate[12].output
        # self.ngate[14].input = self.ngate[13].output
        self.tgate[2].ctop = nxx
        self.tgate[2].cmid = xx
        self.tgate[2].itop = self.C
        self.tgate[2].ilow = self.A
        self.__carry = self.tgate[2].output

        


    @property
    def change_flag(self):
        return any([i.change_flag for i in self.elements])

    @property
    def sum(self):
        self.netlist()
        while self.change_flag:
            self.netlist()
            # [print(i) for i in self.elements]
        return self.__sum
    
    @property
    def carry(self):
        self.netlist()
        while self.change_flag:
            self.netlist()
        return self.__carry

def test_FA():
    fa = FA()

    for i in range(2):
        for j in range(2):
            for k in range(2):
                fa.A = i
                fa.B = j
                fa.C = k

                if (fa.sum == (i+j+k)%2) and (fa.carry == (i+j+k)//2):
                    print(f"{i}, {j}, {k} \t= \t{(i+j+k)//2} \t{(i+j+k)%2} \t[TRUE]")
                else:
                    print("[FALSE]")


# Multiplier 4 bit
class MP4():

    def __init__(self) -> None:
        self.A = [N for _ in range(4)]
        self.B = [N for _ in range(4)]
        self.__output = [N for _ in range(8)]

        self.gand = [And() for _ in range(4*4)]
        self.gfa = [FA() for _ in range(3*4)]

        self.elements = self.gand + self.gfa

    
    def netlist(self):
        
        for lay in range(3):
            for i in range(4):
                self.gand[lay*4 + i].A = self.A[i]
                self.gand[lay*4 + i].B = self.B[lay + 1]

        lay = 3
        for i in range(4):
            self.gand[lay*4 + i].A = self.A[i]
            self.gand[lay*4 + i].B = self.B[0]


        for lay in range(3):
            for i in range(4):
                __A = self.gand[lay*4 + i].output
                if lay != 0:
                    __B = self.gfa[(lay-1)*4 + i + 1].sum if (i!=3) else self.gfa[(lay-1)*4 + i].carry
                else:
                    __B = self.gand[3*4 + i + 1].output if (i!=3) else L
                __C = self.gfa[lay*4 + i - 1].carry if (i!=0) else L

                self.gfa[lay*4 + i].A = __A
                self.gfa[lay*4 + i].B = __B
                self.gfa[lay*4 + i].C = __C


        self.__output[0] = self.gand[3*4 + 0].output
        self.__output[1] = self.gfa[0*4 + 0].sum
        self.__output[2] = self.gfa[1*4 + 0].sum
        self.__output[3] = self.gfa[2*4 + 0].sum
        self.__output[4] = self.gfa[2*4 + 1].sum
        self.__output[5] = self.gfa[2*4 + 2].sum
        self.__output[6] = self.gfa[2*4 + 3].sum
        self.__output[7] = self.gfa[2*4 + 3].carry


    @property
    def change_flag(self):
        return any([i.change_flag for i in self.elements])
    
    @property
    def output(self):
        self.netlist()
        while self.change_flag:
            self.netlist()
        return self.__output




# Multiplier 4 bit
class MP4_manipulated():

    def __init__(self) -> None:
        self.A = [N for _ in range(4)]
        self.B = [N for _ in range(4)]
        self.__output = [N for _ in range(8)]

        self.gand = [And() for _ in range(4*4)]
        self.gfa = [FA() for _ in range(3*4)]

        self.elements = self.gand + self.gfa

    
    def netlist(self):
        
        for lay in range(3):
            for i in range(4):
                self.gand[lay*4 + i].A = self.A[i]
                self.gand[lay*4 + i].B = self.B[lay + 1]

        lay = 3
        for i in range(4):
            self.gand[lay*4 + i].A = self.A[i]
            self.gand[lay*4 + i].B = self.B[0]


        for lay in range(3):
            for i in range(4):
                __A = __B = __C = 0

                __A = self.gand[lay*4 + i].output
                if lay != 0:
                    __B = self.gfa[(lay-1)*4 + i + 1].sum if (i!=3) else self.gfa[(lay-1)*4 + i].carry
                else:
                    __B = self.gand[3*4 + i + 1].output if (i!=3) else L
                __C = self.gfa[lay*4 + i - 1].carry if (i!=0) else L


                # rewiring
                # flip BC {1, 2, 6, 10}
                # flip AC {0, 3, 7, 11}
                # if ((lay*4 + i) in [1, 4, 5, 8, 9, 10]):
                #     self.gfa[lay*4 + i].A = __A
                #     self.gfa[lay*4 + i].B = __C
                #     self.gfa[lay*4 + i].C = __B
                # elif ((lay*4 + i) in [0, 11]):
                #     self.gfa[lay*4 + i].A = __C
                #     self.gfa[lay*4 + i].B = __B
                #     self.gfa[lay*4 + i].C = __A
                if (lay*4 + i) in [9]:
                    self.gfa[lay*4 + i].A = __C 
                    self.gfa[lay*4 + i].B = __B 
                    self.gfa[lay*4 + i].C = __A 
                else:
                    self.gfa[lay*4 + i].A = __A
                    self.gfa[lay*4 + i].B = __B
                    self.gfa[lay*4 + i].C = __C
        


        self.__output[0] = self.gand[3*4 + 0].output
        self.__output[1] = self.gfa[0*4 + 0].sum
        self.__output[2] = self.gfa[1*4 + 0].sum
        self.__output[3] = self.gfa[2*4 + 0].sum
        self.__output[4] = self.gfa[2*4 + 1].sum
        self.__output[5] = self.gfa[2*4 + 2].sum
        self.__output[6] = self.gfa[2*4 + 3].sum
        self.__output[7] = self.gfa[2*4 + 3].carry


    @property
    def change_flag(self):
        return any([i.change_flag for i in self.elements])
    
    @property
    def output(self):
        self.netlist()
        while self.change_flag:
            self.netlist()
        return self.__output




# Multiplier n bit
class MPn:
    def __init__(self, in_len=8) -> None:
        self.in_len = in_len
        self.A = [N for _ in range(in_len)]
        self.B = [N for _ in range(in_len)]
        self.__output = [N for _ in range(in_len*2)]

        self.gand = [And() for _ in range(in_len**2)]
        self.gfa = [FA() for _ in range((in_len-1) * in_len)]

        self.elements = self.gand + self.gfa

    
    def netlist(self):
        
        for lay in range(self.in_len - 1):
            for i in range(self.in_len):
                self.gand[lay*self.in_len + i].A = self.A[i]
                self.gand[lay*self.in_len + i].B = self.B[lay + 1]

        lay = self.in_len-1
        for i in range(self.in_len):
            self.gand[lay*self.in_len + i].A = self.A[i]
            self.gand[lay*self.in_len + i].B = self.B[0]


        for lay in range(self.in_len - 1):
            for i in range(self.in_len):
                __A = self.gand[lay*self.in_len + i].output
                if lay != 0:
                    __B = self.gfa[(lay-1)*self.in_len + i + 1].sum if (i!=(self.in_len-1)) else self.gfa[(lay-1)*self.in_len + i].carry
                else:
                    __B = self.gand[(self.in_len-1)*self.in_len + i + 1].output if (i!=(self.in_len-1)) else L
                __C = self.gfa[lay*self.in_len + i - 1].carry if (i!=0) else L

                self.gfa[lay*self.in_len + i].A = __A
                self.gfa[lay*self.in_len + i].B = __B
                self.gfa[lay*self.in_len + i].C = __C


        self.__output[0] = self.gand[(self.in_len-1)*self.in_len + 0].output
        for lay in range(self.in_len - 1):
            self.__output[lay + 1] = self.gfa[lay*self.in_len + 0].sum

            # last layer
            if lay == self.in_len - 2:
                for i in range(self.in_len + 1):
                    self.__output[lay + i + 1] = self.gfa[lay*self.in_len + i].sum if (i!=self.in_len) else self.gfa[lay*self.in_len + i - 1].carry


    @property
    def change_flag(self):
        return any([i.change_flag for i in self.elements])
    
    @property
    def output(self):
        self.netlist()
        while self.change_flag:
            self.netlist()
        return self.__output




class MPn_v2:
    def __init__(self, A: list[int], B: list[int], in_len=8) -> None:
        self.in_len = in_len
        self.A = A.copy()
        self.B = B.copy()
        self.__output = [N for _ in range(in_len*2)]

        self.gfa = [[FA() for _ in range(in_len)] for _ in range(in_len-1)]
        self.gand = [[And() for _ in range(in_len)] for _ in range(in_len)]

        self.elements = []
        for i in self.gfa:
            self.elements += i
        for i in self.gand:
            self.elements += i

    
    def netlist(self):
        
        # AND input map
        for lay in range(self.in_len):
            for i in range(self.in_len):
                self.gand[lay][i].A = self.A[i]
                self.gand[lay][i].B = self.B[lay]

        # FA input map
        for lay in range(self.in_len-1):
            for i in range(self.in_len):
                __A = self.gand[lay+1][i].output
                if lay == 0:
                    __B = self.gand[0][i+1].output if (i!=self.in_len-1) else L
                else:
                    __B = self.gfa[lay-1][i+1].sum if (i!=self.in_len-1) else self.gfa[lay-1][i].carry
                __C = self.gfa[lay][i-1].carry if (i!=0) else L

                self.gfa[lay][i].A = __A
                self.gfa[lay][i].B = __B
                self.gfa[lay][i].C = __C

        # OUT map
        self.__output[0] = self.gand[0][0].output
        for lay in range(self.in_len -1):
            self.__output[lay + 1] = self.gfa[lay][0].sum

            # last layer
            if lay == self.in_len - 2:
                for i in range(self.in_len + 1):
                    self.__output[lay + i + 1] = self.gfa[lay][i].sum if (i!=self.in_len) else self.gfa[lay][i-1].carry


    @property
    def change_flag(self):
        return any([i.change_flag for i in self.elements])
    
    @property
    def output(self):
        self.netlist()
        while self.change_flag:
            self.netlist()
        return self.__output


# supports 2's compliment numbers
class MPn_v3:
    def __init__(self, A: list[int], B: list[int], in_len=8) -> None:
        self.in_len = in_len
        self.A = A.copy()
        self.B = B.copy()
        self.__output = [N for _ in range(in_len*2)]

        self.gfa = [[FA() for _ in range(in_len)] for _ in range(in_len-1)]
        self.gfa_carry_out = FA()
        self.gand = [[And() for _ in range(in_len)] for _ in range(in_len)]

        self.elements = []
        for i in self.gfa:
            self.elements += i
        for i in self.gand:
            self.elements += i
        self.elements += [self.gfa_carry_out]

    
    def netlist(self):
        
        # AND input map
        for lay in range(self.in_len):
            for i in range(self.in_len):
                self.gand[lay][i].A = self.A[i]
                self.gand[lay][i].B = self.B[lay]

        # FA input map
        for lay in range(self.in_len-1):
            for i in range(self.in_len):
                
                __A = self.gand[lay+1][i].output
                if (lay != self.in_len -1 -1) and (i == self.in_len -1):
                    __A = H if __A==L else L
                elif (lay == self.in_len -1 -1) and (i != self.in_len -1):
                    __A = H if __A==L else L

                if lay == 0:
                    __B = self.gand[0][i+1].output if (i!=self.in_len-1) else H
                    if (i == self.in_len -1 -1):
                        __B = H if __B==L else L
                else:
                    __B = self.gfa[lay-1][i+1].sum if (i!=self.in_len-1) else self.gfa[lay-1][i].carry
                __C = self.gfa[lay][i-1].carry if (i!=0) else L

                self.gfa[lay][i].A = __A
                self.gfa[lay][i].B = __B
                self.gfa[lay][i].C = __C
        
        self.gfa_carry_out.A = L
        self.gfa_carry_out.B = H
        self.gfa_carry_out.C = self.gfa[self.in_len -1 -1][self.in_len -1].carry

        # OUT map
        self.__output[0] = self.gand[0][0].output
        for lay in range(self.in_len -1):
            self.__output[lay + 1] = self.gfa[lay][0].sum

            # last layer
            if lay == self.in_len - 2:
                for i in range(self.in_len + 1):
                    # self.__output[lay + i + 1] = self.gfa[lay][i].sum if (i!=self.in_len) else self.gfa[lay][i-1].carry
                    self.__output[lay + i + 1] = self.gfa[lay][i].sum if (i!=self.in_len) else self.gfa_carry_out.sum


    @property
    def change_flag(self):
        return any([i.change_flag for i in self.elements])
    
    @property
    def output(self):
        self.netlist()
        while self.change_flag:
            self.netlist()
        return self.__output


# from log import Log
# log = Log("Multiplier.txt", terminal=True)

def __test_MP4():
    pass

def __test_MPn_v2():
    def b(num: int, bit_len: int):
        if num < 0:
            # num = 2**bit_len - abs(num)
            num = 2**bit_len + num
        return list(map(int, reversed(format(num, f'0{bit_len}b'))))

    def reverse_b(binary_list):
        binary_str = ''.join(map(str, reversed(binary_list)))
        num = int(binary_str, 2)
        return num


    bit_len = 4
    for i in range(2**bit_len):
        for j in range(2**bit_len):
            output = reverse_b(
                MPn_v2(b(i,bit_len), b(j, bit_len), bit_len).output
            )
            if output != (i*j):
                return False 
    return True

def __test_MPn_v3():
    def signed_b(num: int, bit_len: int):
        num_cpy = num
        if num < 0:
            # num = 2**bit_len - abs(num)
            num_cpy = 2**bit_len + num
        bit_num = list(map(int, reversed(format(num_cpy, f'0{bit_len}b'))))

        if (num>0) and (bit_num[-1] != 0):
            raise OverflowError(f"number {num} cant fit in signed #{bit_len} bits")
        if (num<0) and (bit_num[-1] != 1):
            raise OverflowError(f"number {num} cant fit in signed #{bit_len} bits")
        return bit_num

    def reverse_signed_b(binary_list):
        binary_str = ''.join(map(str, reversed(binary_list)))
        num = int(binary_str, 2)

        #number is negative
        if binary_list[-1] == 1:
            num = num - (2**len(binary_list))
        return num
    
    bit_len = 6
    _range = range(-1*2**(bit_len-1), 2**(bit_len-1))
    for i in _range:
        for j in _range:
            output_bin = MPn_v3(signed_b(i,bit_len), signed_b(j, bit_len), bit_len).output
            output = reverse_signed_b(output_bin)

            # log.println(f"{i} ({signed_b(i, bit_len)}) * {j} ({signed_b(j, bit_len)}) = {output} ({output_bin})")
            if output != (i*j):
                # log.println("[FAILED] (return False)")
                return False 
    return True

if __name__ == "__main__":

    # trans = Trans()
    # trans.ctop = L
    # trans.cmid = H
    # trans.itop = L
    # trans.ilow = H

    # print(trans.output)

    # fa = FA()
    # fa.A = H
    # fa.B = H
    # fa.C = H
    # print(fa.sum)
    # print(fa.carry)


    # m8 = MP4()
    # m8.A = [1,1,1,1]
    # m8.B = [1,1,1,1]
    # print(m8.output)

    #TODO: add test functions

    # test FA
    print("### test FA")
    test_FA()
    print("### test FA DONE")

    # print(f"### test MPn_v2: {__test_MPn_v2()}")
    print(f"### test MPn_v3: {__test_MPn_v3()}")

        



    
    
