from typing import List
import random

import log
log = log.Log(terminal=False)

# import sys
# sys.path.insert(0, '../')
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




if False:
    bit_len = 8

    stress_counter = [[{'T0':0, 'T1':0, 'T2':0} for _ in range(bit_len)] for _ in range(bit_len-1)]
    MP8_input_list = generate_MP_input_pattern(bit_len=bit_len)
    input_len = len(MP8_input_list)

    # show percentage of process
    _precentage_process = 0
    _show_process_counter = 0

    for pattern in MP8_input_list:
        A = pattern['A']
        B = pattern['B']
        mp = MPn_v2(A, B, in_len=bit_len)
        mp.output

        # testing
        if True:
            if mp.output != pattern['output']:
                raise ValueError("wrong output")
            # print testing
            elif False:
                print(f"{A} * {B} \t= {mp.output} \t[{'TRUE' if mp.output == pattern['output'] else 'FALSE'}]")
        
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

            print(f"FA[{lay}][{index}]: {stress} {[i/input_len for i in stress.values()]}")





def not_lst(data_in):
    return [[1,0][i] for i in data_in]

import random
random.seed(0)
def reset_random_chance():
    random.seed(0)

def get_random_chance(chance):
    return random.random() <= chance








bit_len = 6


import matplotlib.pyplot as plt
# plot variables
fig, axes = plt.subplots(bit_len-1, bit_len, figsize=(10, 15))
plt_y = [[0 for _ in range(bit_len)] for _ in range(bit_len-1)]
plt_x = []

if True:
    
    # for XOR_percentage in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.9, 1.0]:
    for XOR_percentage in [0, 1]:
        print(f"XOR percentage: {XOR_percentage}")


        stress_counter = [[{'T0':0, 'T1':0, 'T2':0} for _ in range(bit_len)] for _ in range(bit_len-1)]
        MP8_input_list = generate_MP_input_pattern(bit_len=bit_len)
        input_len = len(MP8_input_list)

        # show percentage of process
        _precentage_process = 0
        _show_process_counter = 0


        reset_random_chance()
        for pattern in MP8_input_list:
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
            if XOR_percentage and (mp.gfa[4][5].tgate[1].p0.gate == L):
                # if XOR help, use XOR on input
                not_A = not_lst(A)
                not_B = not_lst(B)
                mp_xor = MPn_v2(not_A, not_B, in_len=bit_len)
                mp_xor.output

                if (mp_xor.gfa[4][5].tgate[1].p0.gate == H):
                    mp = mp_xor
                else:
                    log.println(f"{A} {B} [using XOR]")



            # testing
            if False:
                if True:
                    print(f"{A} * {B} \t= {output} ({pattern['output']}) \t[{'TRUE' if output == pattern['output'] else 'FALSE'}]")

                if output != pattern['output']:
                    raise ValueError("wrong output")
            
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

                print(f"FA[{lay}][{index}]: {stress} {[i/input_len for i in stress.values()]}")

                try:
                    plt_y[lay][index].append(stress_counter[lay][index])
                except:
                    plt_y[lay][index] = [stress_counter[lay][index]]


        # plot variables
        # plt_y.append(stress_counter[4][1])
        plt_x.append(XOR_percentage)
    

    for lay in range(bit_len-1):
        for index in range(bit_len):
            ax = axes[lay, index]
            ax.plot(plt_x, [i['T0']/input_len for i in plt_y[lay][index]], label="T0")
            ax.plot(plt_x, [i['T1']/input_len for i in plt_y[lay][index]], label="T1")
            ax.plot(plt_x, [i['T2']/input_len for i in plt_y[lay][index]], label="T2")
            ax.set_title(f"FA[{lay}][{index}]")
            # ax.set_xlabel(xlabel)
            # ax.set_ylabel(ylabel)

    # plt.plot(plt_x, [i['T0']/input_len for i in plt_y], label="T0")
    # plt.plot(plt_x, [i['T1']/input_len for i in plt_y], label="T1")
    # plt.plot(plt_x, [i['T2']/input_len for i in plt_y], label="T2")
    plt.legend()
    plt.tight_layout()
    plt.show()


