from Multiplier import *



class org_FA:

    def __init__(self, A=N, B=N, C=N) -> None:
        self.A = A
        self.B = B
        self.C = C

        self.__sum = N
        self.__carry = N

        self.gnot = [Not() for _ in range(4)]
        self.gt = [Trans() for _ in range(3)]
        
        self.elements = self.gnot + self.gt

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
    
    def netlist(self):

        # not A B C
        self.gnot[0].input = self.A
        self.gnot[1].input = self.B
        self.gnot[2].input = self.C
        nA = self.gnot[0].output
        nB = self.gnot[1].output
        nC = self.gnot[2].output

        # xx
        self.gt[0].ctop = self.B
        self.gt[0].cmid = nB
        self.gt[0].itop = self.A
        self.gt[0].ilow = nA
        xx = self.gt[0].output
        
        # nxx
        self.gnot[3].input = xx
        nxx = self.gnot[3].output

        # sum
        self.gt[1].ctop = xx
        self.gt[1].cmid = nxx
        self.gt[1].itop = self.C
        self.gt[1].ilow = nC
        self.__sum = self.gt[1].output

        # carry
        self.gt[2].ctop = nxx
        self.gt[2].cmid = xx
        self.gt[2].itop = self.C
        self.gt[2].ilow = self.A
        self.__carry = self.gt[2].output



def test_FA():
    fa = org_FA()

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

print("################## TEST FA")
test_FA()
print("################## TEST FA DONE")

    


class MP3:

    def __init__(self, A = False, B = False) -> None:
        self.in_len = 3
        self.A = [N for _ in range(self.in_len)] if not A else A
        self.B = [N for _ in range(self.in_len)] if not B else B
        self.__output = [N for _ in range(self.in_len * 2)]

        self.gFA = [[org_FA() for i in range(self.in_len)] for _ in range(self.in_len - 1)]
        self.gAND = [[And() for i in range(self.in_len)] for _ in range(self.in_len)]

        self.elements = self.gAND[0] + self.gAND[1] + self.gAND[2] + self.gFA[0] + self.gFA[1]



    def netlist(self):
        
        # AND input
        for lay in range(self.in_len):
            for i in range(self.in_len):
                self.gAND[lay][i].A = self.A[i]
                self.gAND[lay][i].B = self.B[lay]


        # FA input
        for lay in range(self.in_len - 1):
            for i in range(self.in_len):
                __A = self.gAND[lay+1][i].output
                if lay == 0:
                    __B = self.gAND[0][i+1].output if (i!=self.in_len-1) else L
                else:
                    __B = self.gFA[lay-1][i+1].sum if (i!=self.in_len-1) else self.gFA[lay-1][i].carry
                __C = self.gFA[lay][i-1].carry if (i!=0) else L

                self.gFA[lay][i].A = __A
                self.gFA[lay][i].B = __C
                self.gFA[lay][i].C = __B


        self.__output[0] = self.gAND[0][0].output
        self.__output[1] = self.gFA[0][0].sum
        self.__output[2] = self.gFA[1][0].sum
        self.__output[3] = self.gFA[1][1].sum
        self.__output[4] = self.gFA[1][2].sum
        self.__output[5] = self.gFA[1][2].carry


    @property
    def change_flag(self):
        return any([i.change_flag for i in self.elements])
    

    @property
    def output(self):
        self.netlist()
        while self.change_flag:
            self.netlist()
        return self.__output



def generate_MP_input_pattern():
    input_pattern = []
    for A in range(0, 0b111 + 1):
        for B in range(0, 0b111 + 1):
            def b(num: int, length: int = 3):
                return list(map(int, reversed(format(num, f'0{length}b'))))
            input_pattern += [{'A': b(A), 'B': b(B), 'output': b(A*B, 6)}]
    return input_pattern

def test_MP():
    input_pattern = generate_MP_input_pattern()
    for pattern in input_pattern:

        mp = MP3()

        mp.A = pattern['A']
        mp.B = pattern['B']

        mp_out = mp.output

        if (mp_out == pattern['output']):
            print(f"\t{mp.A} * \t{mp.B} = \t{mp_out} [TRUE]")
        else:
            print(f"\t{mp.A} * \t{mp.B} = \t{mp_out} (expected: {pattern['output']}) [FALSE]")
            return False
    return True



def MP3_counter(MP3_list):
    A = [0 for i in range(3)]
    B = [0 for i in range(3)]
    output = [0 for i in range(6)]

    gand = [[{'A':0, 'B':0} for i in range(3)] for j in range(3)]
    gfa = [[{'A':0, 'B':0, 'C':0, 'sum':0, 'carry':0} for i in range(3)] for j in range(2)]

    usr_counter = 0

    for mp3 in MP3_list:
        mp3: MP3
        mp3.output

        # # input
        # for i in range(3):
        #     A[i] += 1 if mp3.A[i] else 0
        #     B[i] += 1 if mp3.B[i] else 0
        
        # # output
        # for i in range(6):
        #     output[i] += 1 if mp3.output[i] else 0

        # # and gate
        # for i in range(3):
        #     for j in range(3):
        #         gand[i][j]['A'] += 1 if mp3.gAND[i][j].A else 0
        #         gand[i][j]['B'] += 1 if mp3.gAND[i][j].B else 0
        
        # # FA 
        # for i in range(2):
        #     for j in range(3):
        #         gfa[i][j]['A'] += 1 if mp3.gFA[i][j].A else 0
        #         gfa[i][j]['B'] += 1 if mp3.gFA[i][j].B else 0
        #         gfa[i][j]['C'] += 1 if mp3.gFA[i][j].C else 0
        #         gfa[i][j]['sum'] += 1 if mp3.gFA[i][j].sum else 0
        #         gfa[i][j]['carry'] += 1 if mp3.gFA[i][j].carry else 0

        usr_counter += 1 if mp3.gFA[1][1].gt[0].p0.gate == L else 0
    print(f"usr_counter: \t{usr_counter}")

    
    print("DONE")
        
        
        


print("##################### TEST MP")
test_MP()
print("##################### TEST MP DONE")

mp_list = [MP3(A=i['A'], B=i['B']) for i in generate_MP_input_pattern()]
MP3_counter(mp_list)
print("############ COUNTING DONE, see the details in debug mode")