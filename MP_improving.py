from Multiplier import *
from typing import List
import random



def generate_MP_input_pattern(bit_len):
    input_pattern = []
    for A in range(0, 2**bit_len):
        for B in range(0, 2**bit_len):
            def b(num: int, length: int = bit_len):
                return list(map(int, reversed(format(num, f'0{length}b'))))
            input_pattern += [{'A': b(A), 'B': b(B), 'output': b(A*B, bit_len*2)}]
    return input_pattern


def counter(ll):
    count_dict = {}

    for i in ll:
        if str(i) in count_dict:
            count_dict[str(i)] += 1
        else:
            count_dict[str(i)] = 1
        
    return count_dict







# MP4_input_list = generate_MP_input_pattern(bit_len=4)
# MP4_list = []
# print("### generating MP4 list")
# for _input in MP4_input_list:
#     A = _input['A']
#     B = _input['B']
#     output = _input['output']

#     mp4 = MP4()
#     mp4.A = A
#     mp4.B = B
#     _ = mp4.output

#     MP4_list.append(mp4)

#     # testing MP4
#     if False:
#         print(f"A:{A},\t B:{B},\t {mp4.output} == {output} \t\t[{'True' if mp4.output == output else 'FALSE'}]")
# print("### genetating MP4 DONE")


MP8_input_list = generate_MP_input_pattern(bit_len=8)
MP8_list = []
test_counter = 0
test_counter_list = sorted(random.sample(range((2**16) +1), 1000))
print("### generating MP8 list")
for _input in MP8_input_list:
    A = _input['A']
    B = _input['B']
    output = _input['output']

    mp8 = MPn(in_len=8)
    mp8.A = A
    mp8.B = B
    _ = mp8.output

    MP8_list.append(mp4)

    # teting MP4
    if True:
        test_counter += 1
        if test_counter in test_counter_list:
            print(f"[{test_counter:04}/{2**16}] A:{A}, B:{B},\t {mp8.output} == {output} [{'True' if mp8.output == output else 'FALSE'}]")
print("### generating MP8 DONE")




# i = MP4()

# i.gand[0].output

# print('and: ', counter([[i.gand[0].output] for i in MP4_list]))

# print(counter(
#     [[i.gfa[8].B] for i in MP4_list]
# ))


# for index in range(4*3):
#     MP4_list: List[MP4]

#     A = counter([[i.gfa[index].A] for i in MP4_list])
#     B = counter([[i.gfa[index].B] for i in MP4_list])
#     C = counter([[i.gfa[index].C] for i in MP4_list])

#     print(f"MP4[{index:02}] A: {A}")
#     print(f"MP4[{index:02}] B: {B}")
#     print(f"MP4[{index:02}] C: {C}")



#     # does flipping AB will result in more balance ?
#     # B balance metric
#     balance_B = B.get('[0]', 0) - B.get('[1]', 0)
#     # A balance metric
#     balance_A = A.get('[0]', 0) - A.get('[1]', 0)

#     print(f"is it critical path: [{'YES' if index in [0,1,4,5,8,9,10,11] else 'NO'}]")
#     print(f"flip AB: [{'YES' if balance_A < balance_B else 'NO'}]")
#     print(f"change due to flip: [{(A.get('[0]') - B.get('[0]')) / B.get('[0]') * 100 :02.1f}%]")

#     print()
#     print('-'*10)


for index in range(8*7):
    MP8_list: List[MP8_list[0]]

    A = counter([[i.gfa[index].A] for i in MP8_list])
    B = counter([[i.gfa[index].B] for i in MP8_list])
    C = counter([[i.gfa[index].C] for i in MP8_list])

    print(f"MP8[{index:02}] A: {A}")
    print(f"MP8[{index:02}] B: {B}")
    print(f"MP8[{index:02}] C: {C}")



    # does flipping AB will result in more balance ?
    # B balance metric
    balance_B = B.get('[0]', 0) - B.get('[1]', 0)
    # A balance metric
    balance_A = A.get('[0]', 0) - A.get('[1]', 0)

    print(f"is it critical path: [{'YES' if index in [0,1,4,5,8,9,10,11] else 'NO'}]")
    print(f"flip AB: [{'YES' if balance_A < balance_B else 'NO'}]")
    print(f"change due to flip: [{(A.get('[0]') - B.get('[0]')) / B.get('[0]') * 100 :02.1f}%]")

    print()
    print('-'*10)