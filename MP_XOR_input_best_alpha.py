from typing import List
import matplotlib.pyplot as plt

from Multiplier import *

import log
log = log.Log(terminal=False)


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


def not_lst(data_in):
    return [[1,0][i] for i in data_in]


def get_max_alpha(stress_counter, bit_len):
    max_fa_i = 0
    max_fa_j = 0
    max_fa_t = 0
    _max_alpha = 0

    for fa_i in range(bit_len):
        for fa_j in range(bit_len-1):
            for t_index in range(3):

                _alpha = stress_counter[fa_i][fa_j][f'T{t_index}']
                if _max_alpha < _alpha:
                    _max_alpha = +_alpha
                    max_fa_i = fa_i
                    max_fa_j = fa_j
                    max_fa_t = t_index
    return [max_fa_i, max_fa_j, max_fa_t, _max_alpha]

bit_len = 6

best_mp = MPn_v2(A=[1,0,0,0,0,0], B=[1,1,1,1,1,1], in_len=bit_len)


stress_counter = 0
def reset_stress_counter():
    global stress_counter
    stress_counter = [[{'T0':0, 'T1':0, 'T2':0} for _ in range(bit_len)] for _ in range(bit_len-1)]
reset_stress_counter()

MP_input_list = generate_MP_input_pattern(bit_len=bit_len)
input_len = len(MP_input_list)

# show percentage of process
_precentage_process = 0
_show_process_counter = 0


for pattern in MP_input_list:
    A = pattern['A']
    B = pattern['B']

    # xor_enable = get_random_chance(XOR_percentage)
    # if xor_enable:
    #     A = not_lst(A)
    #     B = not_lst(B)

    mp = MPn_v2(A, B, in_len=bit_len)
    output = mp.output
    # if xor_enable:
    #     output = not_lst(output)

    # optimizer to reduce the stress
    if ((mp.gfa[1][5].tgate[0].p0.gate == L) or (mp.gfa[2][5].tgate[0].p0.gate == L)):
        # if XOR help, use XOR on input
        not_A = not_lst(A)
        not_B = not_lst(B)
        mp_xor = MPn_v2(not_A, not_B, in_len=bit_len)
        mp_xor.output

        if (mp_xor.gfa[1][5].tgate[0].p0.gate == H) or ((mp.gfa[2][5].tgate[0].p0.gate == H)):
            mp = mp_xor
        else:
            log.println(f"{A} {B} [using XOR]")

    
    # show process
    _show_process_counter += 1
    _current_percentage = round(_show_process_counter/input_len*100)
    if _current_percentage > _precentage_process:
        _precentage_process = _current_percentage
        print(f"[{_current_percentage:03}%]")

    for lay in range(bit_len-1):
        for index in range(bit_len):

            T0 = mp.gfa[lay][index].tgate[0].p0.gate
            T1 = mp.gfa[lay][index].tgate[1].p0.gate
            T2 = mp.gfa[lay][index].tgate[2].p1.gate

            if T0 == L:
                stress_counter[lay][index]['T0'] += 1
            if T1 == L:
                stress_counter[lay][index]['T1'] += 1
            if T2 == L:
                stress_counter[lay][index]['T2'] += 1


for lay in range(bit_len-1):
    for index in range(bit_len):

        stress = stress_counter[lay][index]

        log.println(f"FA[{lay}][{index}]: {stress} {[i/input_len for i in stress.values()]}")



    