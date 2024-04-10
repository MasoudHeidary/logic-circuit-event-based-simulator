from Multiplier import *


input_patterns = []
for A in range(0xF + 1):
    for B in range(0xF + 1):
        def _(num: int, length: int = 4):
            return list(map(int, reversed(format(num, f'0{length}b'))))
        input_patterns += [{'A': _(A), 'B': _(B)}]











class MPCounter:
    def __init__(self) -> None:
        self.tgate_counter = [[0 for j in range(6)] for i in range(12)]
        self.ngate_counter = [[0 for j in range(15)] for i in range(12)]
        self.andgate_counter = [[0, 0, 0] for _ in range(16)]

    def ngate(self, mp4: MP4):
        for i_FA, fa in enumerate(mp4.gfa):
            fa: FA
            for i_NOT, ng in enumerate(fa.ngate):
                if(ng.p.gate == L):
                    self.ngate_counter[i_FA][i_NOT] += 1


    def tgate(self, mp4: MP4):
        for i_FA, fa in enumerate(mp4.gfa):
            fa: FA
            for i_t, tg in enumerate(fa.tgate):
                if tg.p0.gate == L:
                    self.tgate_counter[i_FA][i_t*2] += 1
                if tg.p1.gate == L:
                    self.tgate_counter[i_FA][i_t*2 + 1] += 1

    def andgate(self, mp4: MP4):
        for i_andg, andg in enumerate(mp4.gand):
            andg: And
            if andg.p[0].gate == L:
                self.andgate_counter[i_andg][0] += 1
            if andg.p[1].gate == L:
                self.andgate_counter[i_andg][1] += 1
            if andg.ngate.p.gate == L:
                self.andgate_counter[i_andg][2] += 1


        

mp4 = MP4()
mp4_counter = MPCounter()

mp4_mani = MP4_manipulated()
mp4_mani_counter = MPCounter()

for i in range(len(input_patterns)):
    mp4.A = input_patterns[i]['A']
    mp4.B = input_patterns[i]['B']
    mp4.output

    mp4_mani.A = input_patterns[i]['A']
    mp4_mani.B = input_patterns[i]['B']
    mp4_mani.output

    print(f"pattern #{i}/255 DONE")

    mp4_counter.ngate(mp4)
    mp4_counter.tgate(mp4)
    mp4_counter.andgate(mp4)
    mp4_mani_counter.ngate(mp4_mani)
    mp4_mani_counter.tgate(mp4_mani)
    mp4_mani_counter.andgate(mp4_mani)


for i_fa in range(len(mp4_counter.ngate_counter)):
    print('-'*20)
    for i_not in range(len(mp4_counter.ngate_counter[i_fa])):

        normal_ngate = mp4_counter.ngate_counter[i_fa][i_not]
        mani_ngate = mp4_mani_counter.ngate_counter[i_fa][i_not]

        print(f"\
FA {i_fa},\t\t\
Not[{i_not}],\t\t\
Normal {normal_ngate},\t\t\
manipulated {mani_ngate},\t\t\
diff {((mani_ngate - normal_ngate)/normal_ngate * 100) if normal_ngate != 0 else N} %\
            ")


    for i_tgate in range(len(mp4_counter.tgate_counter[i_fa])):
        
        normal_tgate = mp4_counter.tgate_counter[i_fa][i_tgate]
        mani_tgate = mp4_mani_counter.tgate_counter[i_fa][i_tgate]

        print(f"\
FA {i_fa},\t\t\
Tgate[{i_not}],\t\t\
Normal {normal_tgate},\t\t\
manipulated {mani_tgate},\t\t\
diff {((mani_tgate - normal_tgate)/normal_tgate * 100) if normal_tgate != 0 else N} %\
            ")


for i_and in range(len(mp4_counter.andgate_counter)):
    print('-'*15)
    for i_p in range(3):

        normal_andgate = mp4_counter.andgate_counter[i_and][i_p]
        mani_andgate = mp4_mani_counter.andgate_counter[i_and][i_p]


        print(f"\
AND {i_and},\t\t\
p[{i_p}],\t\t\
Normal {normal_andgate},\t\t\
manipulated {mani_andgate},\t\t\
diff {((mani_andgate - normal_andgate)/normal_andgate * 100) if normal_andgate != 0 else N} %\
            ")


