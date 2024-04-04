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

        self.ngate = [Not() for _ in range(15)]
        self.tgate = [Trans() for _ in range(3)]
        self.elements = self.ngate + self.tgate

    def netlist(self):

        # not A B C
        self.ngate[0].input = self.A     #nA
        self.ngate[1].input = self.B     #nB
        self.ngate[2].input = self.C     #nC


        # generate xx signal
        self.tgate[0].ctop = self.B
        self.tgate[0].cmid = self.ngate[1].output
        self.tgate[0].itop = self.A
        self.tgate[0].ilow = self.ngate[0].output
        # generate nxx signal
        self.ngate[3].input = self.tgate[0].output
        # generate dxx
        self.ngate[4].input = self.tgate[0].output
        self.ngate[5].input = self.ngate[4].output


        # generate sum
        self.ngate[6].input = self.ngate[2].output
        self.ngate[7].input = self.ngate[6].output
        self.ngate[8].input = self.ngate[7].output

        self.ngate[9].input = self.ngate[2].output
        self.ngate[10].input = self.ngate[9].output

        self.tgate[1].ctop = self.ngate[5].output
        self.tgate[1].cmid = self.ngate[3].output
        self.tgate[1].itop = self.ngate[8].output
        self.tgate[1].ilow = self.ngate[10].output



        # generate carry 
        self.ngate[11].input = self.A
        self.ngate[12].input = self.ngate[11].output
        self.ngate[13].input = self.ngate[12].output
        self.ngate[14].input = self.ngate[13].output
        self.tgate[2].ctop = self.ngate[3].output
        self.tgate[2].cmid = self.ngate[5].output
        self.tgate[2].itop = self.C
        self.tgate[2].ilow = self.ngate[14].output

        
        self.__sum = self.tgate[1].output
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
                self.gfa[lay*4 + i].A = self.gand[lay*4 + i].output
                if lay != 0:
                    self.gfa[lay*4 + i].B = self.gfa[(lay-1)*4 + i + 1].sum if (i!=3) else self.gfa[(lay-1)*4 + i].carry
                else:
                    self.gfa[lay*4 + i].B = self.gand[3*4 + i + 1].output if (i!=3) else L
                self.gfa[lay*4 + i].C = self.gfa[lay*4 + i - 1].carry if (i!=0) else L


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


if __name__ == "__main__":

    trans = Trans()
    trans.ctop = L
    trans.cmid = H
    trans.itop = L
    trans.ilow = H

    print(trans.output)

    fa = FA()
    fa.A = H
    fa.B = H
    fa.C = H
    print(fa.sum)
    print(fa.carry)


    m8 = MP4()
    m8.A = [1,1,1,1]
    m8.B = [1,1,1,1]
    print(m8.output)

    #TODO: add test functions



        



    
    
