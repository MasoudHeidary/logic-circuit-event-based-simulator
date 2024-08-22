from typing import List
import random

import sys
sys.path.insert(0, '..')
from Multiplier import *

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






bit_len = 4
improvement = 0

MP4_input_list = generate_MP_input_pattern(bit_len=bit_len)
MP4_list = []
print("### generating MP4 list")
for _input in MP4_input_list:
    A = _input['A']
    B = _input['B']
    output = _input['output']

    mp4 = MP4()
    mp4.A = A
    mp4.B = B
    _ = mp4.output

    MP4_list.append(mp4)

    # testing MP4
    if False:
        print(f"A:{A},\t B:{B},\t {mp4.output} == {output} \t\t[{'True' if mp4.output == output else 'FALSE'}]")
print("### genetating MP4 DONE")



for index in range(bit_len*(bit_len-1)):
    MP4_list: List[MP4]

    A = counter([[i.gfa[index].A] for i in MP4_list])
    B = counter([[i.gfa[index].B] for i in MP4_list])
    C = counter([[i.gfa[index].C] for i in MP4_list])

    print(f"MP4[{index:02}] A: {A}")
    print(f"MP4[{index:02}] B: {B}")
    print(f"MP4[{index:02}] C: {C}")



    # does flipping AB will result in more balance ?
    # B balance metric
    balance_B = B.get('[0]', 0) - B.get('[1]', 0)
    # A balance metric
    balance_A = A.get('[0]', 0) - A.get('[1]', 0)

    print(f"is it critical path: [{'YES' if index in [0,1, 4,5, 8,9,10,11] else 'NO'}]")
    print(f"flip AB: [{'YES' if balance_A < balance_B else 'NO'}]")
    print(f"change due to flip: [{(A.get('[0]') - B.get('[0]')) / B.get('[0]') * 100 :02.1f}%]")

    if (balance_A < balance_B) and (index in [0,1, 4,5, 8,9,10,11]):
        improvement += ((A.get('[0]') - B.get('[0]')) / B.get('[0]') * 100)

    print()
    print('-'*10)
print(f"MP4 improvement: {improvement:02.1f}%")

# =======================================================================================================

bit_len = 5
improvement = 0

MP8_input_list = generate_MP_input_pattern(bit_len=bit_len)
# MP8_list = []
test_counter = 0
test_counter_list = sorted(random.sample(range((2**(2*bit_len)) +1), 500))

gfa_len = bit_len*(bit_len-1)
gfa_counter = [{'A':0, 'B':0, 'C':0} for _ in range(gfa_len)]

print("### generating MP5 list")
for _input in MP8_input_list:
    A = _input['A']
    B = _input['B']
    output = _input['output']

    mp8 = MPn(in_len=bit_len)
    mp8.A = A
    mp8.B = B
    _ = mp8.output

    # teting
    if False:
        test_counter += 1
        if test_counter in test_counter_list:
            print(f"[{test_counter/(2**(2*bit_len))*100:02.1f}%][{test_counter:04}/{2**(2*bit_len)}] A:{A}, B:{B},\t {mp8.output} == {output} [{'True' if mp8.output == output else 'FALSE'}]")


    for i in range(gfa_len):
        
        A = mp8.gfa[i].A
        B = mp8.gfa[i].B
        C = mp8.gfa[i].C

        if A == L:
            gfa_counter[i]['A'] += 1
        if B == L:
            gfa_counter[i]['B'] += 1
        if C == L:
            gfa_counter[i]['C'] += 1

print("### generating MP5 DONE")


critical_path = [0,1, 5,6, 10,11, 15,16,17,18,19]
# for index in range(gfa_len):
for index in critical_path:

    A = gfa_counter[index]['A']
    B = gfa_counter[index]['B']
    C = gfa_counter[index]['C']

    print(f"FA[{index}]: ABC {gfa_counter[index]}")

    print(f"is it critical path: [{'YES' if index in critical_path else 'NO'}]")
    print(f"flip AB: [{'YES' if A < B else 'NO'}] [{(A - B) / B * 100 :02.1f}%]")
    print(f"flip BC: [{'YES' if C < B else 'NO'}] [{(C - B) / B * 100 :02.1f}%]")

    if A < B:
        improvement += ((A - B) / B * 100)

    print()
    print('='*20)
print(f"MP5 improvement: {improvement:02.1f}%")


# =======================================================================================================

bit_len = 6
improvement = 0

MP8_input_list = generate_MP_input_pattern(bit_len=bit_len)
# MP8_list = []
test_counter = 0
test_counter_list = sorted(random.sample(range((2**(2*bit_len)) +1), 500))

gfa_len = bit_len*(bit_len-1)
gfa_counter = [{'A':0, 'B':0, 'C':0} for _ in range(gfa_len)]

print("### generating MP6 list")
for _input in MP8_input_list:
    A = _input['A']
    B = _input['B']
    output = _input['output']

    mp8 = MPn(in_len=bit_len)
    mp8.A = A
    mp8.B = B
    _ = mp8.output

    # MP8_list.append(mp8)

    # teting MP8
    if False:
        test_counter += 1
        if test_counter in test_counter_list:
            print(f"[{test_counter/(2**(2*bit_len))*100:02.1f}%][{test_counter:04}/{2**(2*bit_len)}] A:{A}, B:{B},\t {mp8.output} == {output} [{'True' if mp8.output == output else 'FALSE'}]")


    for i in range(gfa_len):
        
        A = mp8.gfa[i].A
        B = mp8.gfa[i].B
        C = mp8.gfa[i].C

        if A == L:
            gfa_counter[i]['A'] += 1
        if B == L:
            gfa_counter[i]['B'] += 1
        if C == L:
            gfa_counter[i]['C'] += 1

print("### generating MP6 DONE")

critical_path = [0,1, 6,7, 12,13, 18,19, 24,25,26,27,28,29]
# for index in range(gfa_len):
for index in critical_path:

    A = gfa_counter[index]['A']
    B = gfa_counter[index]['B']
    C = gfa_counter[index]['C']

    print(f"FA[{index}]: ABC {gfa_counter[index]}")

    print(f"is it critical path: [{'YES' if index in critical_path else 'NO'}]")
    print(f"flip AB: [{'YES' if A < B else 'NO'}] [{(A - B) / B * 100 :02.1f}%]")
    print(f"flip BC: [{'YES' if C < B else 'NO'}] [{(C - B) / B * 100 :02.1f}%]")

    if A < B:
        improvement += ((A - B) / B * 100)

    print()
    print('='*20)
print(f"MP6 improvement: {improvement:02.1f}%")


# =======================================================================================================

bit_len = 7
improvement = 0

MP8_input_list = generate_MP_input_pattern(bit_len=bit_len)
# MP8_list = []
test_counter = 0
test_counter_list = sorted(random.sample(range((2**(2*bit_len)) +1), 1000))

gfa_len = bit_len*(bit_len-1)
gfa_counter = [{'A':0, 'B':0, 'C':0} for _ in range(gfa_len)]

print("### generating MP7 list")
for _input in MP8_input_list:
    A = _input['A']
    B = _input['B']
    output = _input['output']

    mp8 = MPn(in_len=bit_len)
    mp8.A = A
    mp8.B = B
    _ = mp8.output

    # MP8_list.append(mp8)

    # teting MP8
    if False:
        test_counter += 1
        if test_counter in test_counter_list:
            print(f"[{test_counter/(2**(2*bit_len))*100:02.1f}%][{test_counter:04}/{2**(2*bit_len)}] A:{A}, B:{B},\t {mp8.output} == {output} [{'True' if mp8.output == output else 'FALSE'}]")


    for i in range(gfa_len):
        
        A = mp8.gfa[i].A
        B = mp8.gfa[i].B
        C = mp8.gfa[i].C

        if A == L:
            gfa_counter[i]['A'] += 1
        if B == L:
            gfa_counter[i]['B'] += 1
        if C == L:
            gfa_counter[i]['C'] += 1

print("### generating MP7 DONE")


critical_path = [0,1, 7,9, 14,15, 21,22, 28,29, 35,36,37,38,39,40,41]
# for index in range(gfa_len):
for index in critical_path:

    A = gfa_counter[index]['A']
    B = gfa_counter[index]['B']
    C = gfa_counter[index]['C']

    print(f"FA[{index}]: ABC {gfa_counter[index]}")

    print(f"is it critical path: [{'YES' if index in critical_path else 'NO'}]")
    print(f"flip AB: [{'YES' if A < B else 'NO'}] [{(A - B) / B * 100 :02.1f}%]")
    print(f"flip BC: [{'YES' if C < B else 'NO'}] [{(C - B) / B * 100 :02.1f}%]")

    if A < B:
        improvement += ((A - B) / B * 100)

    print()
    print('='*20)
print(f"MP7 improvement: {improvement:02.1f}%")



# =======================================================================================================

bit_len = 8
improvement = 0

MP8_input_list = generate_MP_input_pattern(bit_len=bit_len)
# MP8_list = []
test_counter = 0
test_counter_list = sorted(random.sample(range((2**(2*bit_len)) +1), 1000))

gfa_len = bit_len*(bit_len-1)
gfa_counter = [{'A':0, 'B':0, 'C':0} for _ in range(gfa_len)]

print("### generating MP8 list")
for _input in MP8_input_list:
    A = _input['A']
    B = _input['B']
    output = _input['output']

    mp8 = MPn(in_len=bit_len)
    mp8.A = A
    mp8.B = B
    _ = mp8.output

    # MP8_list.append(mp8)

    # teting MP8
    if False:
        test_counter += 1
        if test_counter in test_counter_list:
            print(f"[{test_counter/(2**(2*bit_len))*100:02.1f}%][{test_counter:04}/{2**(2*bit_len)}] A:{A}, B:{B},\t {mp8.output} == {output} [{'True' if mp8.output == output else 'FALSE'}]")


    for i in range(gfa_len):
        
        A = mp8.gfa[i].A
        B = mp8.gfa[i].B
        C = mp8.gfa[i].C

        if A == L:
            gfa_counter[i]['A'] += 1
        if B == L:
            gfa_counter[i]['B'] += 1
        if C == L:
            gfa_counter[i]['C'] += 1

print("### generating MP8 DONE")


critical_path = [0,1, 8,9, 16,17, 24,25, 32,33, 40,41, 48,49,50,51,52,53,54,55]
# for index in range(gfa_len):
for index in critical_path:

    A = gfa_counter[index]['A']
    B = gfa_counter[index]['B']
    C = gfa_counter[index]['C']

    print(f"FA[{index}]: ABC {gfa_counter[index]}")

    print(f"is it critical path: [{'YES' if index in critical_path else 'NO'}]")
    print(f"flip AB: [{'YES' if A < B else 'NO'}] [{(A - B) / B * 100 :02.1f}%]")
    print(f"flip BC: [{'YES' if C < B else 'NO'}] [{(C - B) / B * 100 :02.1f}%]")

    if A < B:
        improvement += ((A - B) / B * 100)

    print()
    print('='*20)
print(f"MP8 improvement: {improvement:02.1f}%")



