from typing import List, Dict
import time
import random
import log

from Multiplier import *

"""
NOTE:
for example in 6bit signed number the range is -32 to +31
but because we flip the sign of numbers to decrease the stress,
we consider the range as -31 to +31
"""

# def b(num: int, bit_len: int):
#     if num < 0:
#         # num = 2**bit_len - abs(num)
#         num = 2**bit_len + num
#     return list(map(int, reversed(format(num, f'0{bit_len}b'))))

# def reverse_b(binary_list):
#     binary_str = ''.join(map(str, reversed(binary_list)))
#     num = int(binary_str, 2)

#     #number is negative
#     if binary_list[-1] == 1:
#         num = num - (2**len(binary_list))
#     return num

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
    

# def random_MP_input_pattern(bit_len, random_seed=-1, length=1) -> List[Dict[str, List[int]]]:
#     input_pattern = []
#     if random_seed != -1:
#         random.seed(random_seed)

#     for _ in range(length):
#         A = random.randint(0, 2**bit_len-1)
#         B = random.randint(0, 2**bit_len-1)
        
#         input_pattern += [
#             {
#                 'A': signed_b(A, bit_len), 
#                 'B': signed_b(B, bit_len), 
#                 'output': signed_b(A*B, bit_len*2)
#             }
#         ]
#     return input_pattern


# def full_MP_input_pattern(bit_len: int):
#     input_pattern = []
    
#     for A in range(0, 2**bit_len):
#         for B in range(0, 2**bit_len):
#             input_pattern += [
#                 {
#                     'A': signed_b(A, bit_len),
#                     'B': signed_b(B, bit_len),
#                     'output': signed_b(A*B, bit_len*2)
#                 }
#             ]
#     return input_pattern

# def yield_full_MP_input_pattern(bit_len: int):
#     for A in range(0, 2**bit_len):
#         for B in range(0, 2**bit_len):
#             yield {
#                 'A': signed_b(A, bit_len),
#                 'B': signed_b(B, bit_len),
#                 'output': signed_b(A*B, bit_len*2)
#             }

# def yield_full_MP_input_number(bit_len: int):
#     for A in range(0, 2**bit_len):
#         for B in range(0, 2**bit_len):
#             yield {
#                 'A': A,
#                 'B': B,
#                 'output': A*B
#             }

def yield_full_MP_signed_input_number(bit_len: int):
    _range = range(-1*2**(bit_len-1), 2**(bit_len-1))
    for A in _range:
        for B in _range:
            yield {
                'A': A,
                'B': B,
                'output': A*B,
            }

# def yield_cut_MP_signed_input_number(bit_len: int):
#     _range = range(-1*2**(bit_len-1) + 1, 2**(bit_len-1))
#     for A in _range:
#         for B in _range:
#             yield {
#                 'A': A,
#                 'B': B,
#                 'output': A*B,
#             }


# =====================================================================================

if __name__ == "__main__":
    bit_len = 8
    OPTIMIZER_ENABLE = True
    start_time = time.time()


    log = log.Log(name=f"log-main_improving_aging_1.txt", terminal=True)
    _note = \
    """
        ######################### OPTIMIZER
        # do not optimize these numbers
        if OPTIMIZER_ENABLE:
            if (A == -1*2**(bit_len-1)) or (B == -1*2**(bit_len-1)):
                pass
            else:
                if (mp.gfa[1][7].tgate[0].p1.gate == L):
                    neg_A = -A
                    neg_B = -B
                    neg_mp = MPn_v3(
                        signed_b(neg_A, bit_len),
                        signed_b(neg_B, bit_len),
                        bit_len
                    )
                    neg_mp.output

                    if (neg_mp.gfa[1][7].tgate[0].p1.gate == H) or (neg_mp.gfa[0][5].tgate[0].p0.gate == H):
                        mp = neg_mp
                        optimized_flag = True
                        # log.println(f"{A} * {B}, [optimizer: {optimized_flag}]")

        ######################### /OPTIMIZER
    """
    log.println(_note)

    input_numbers = yield_full_MP_signed_input_number(bit_len)
    # input_numbers = yield_cut_MP_signed_input_number(bit_len)
    input_len = (2**bit_len)**2

    # show percentage of process
    _precentage_process = 0
    _show_process_counter = 0

    # stress
    stress_counter = [[{'T0':0, 'T0p':0, 'T1':0, 'T1p':0, 'T2':0, 'T2p':0} for _ in range(bit_len)] for _ in range(bit_len-1)]

    
    for input_number in input_numbers:
        # indicate that this iterate trigged optimizer
        optimized_flag = False

        A = input_number['A']
        B = input_number['B']

        mp = MPn_v3(signed_b(A, bit_len), signed_b(B, bit_len), bit_len)
        mp.output

        ######################### OPTIMIZER
        # do not optimize these numbers
        if OPTIMIZER_ENABLE:
            if (A == -1*2**(bit_len-1)) or (B == -1*2**(bit_len-1)):
                pass
            else:
                if (mp.gfa[1][7].tgate[0].p1.gate == L):
                    neg_A = -A
                    neg_B = -B
                    neg_mp = MPn_v3(
                        signed_b(neg_A, bit_len),
                        signed_b(neg_B, bit_len),
                        bit_len
                    )
                    neg_mp.output

                    if (neg_mp.gfa[1][7].tgate[0].p1.gate == H) or (neg_mp.gfa[0][5].tgate[0].p0.gate == H):
                        mp = neg_mp
                        optimized_flag = True
                        # log.println(f"{A} * {B}, [optimizer: {optimized_flag}]")
                        log.println(f"{signed_b(A, bit_len)} ({A})\t\t{signed_b(B, bit_len)} ({B})\t\t [OPTIMIZED FLAG: {optimized_flag}]")

        ######################### /OPTIMIZER

        output = mp.output
        # running test
        if True:
            if output != signed_b(input_number['output'], bit_len*2):
                raise RuntimeError(f"Multiplier test failed, {A}({signed_b(A, bit_len)}) x {B}({signed_b(B, bit_len)}) \
                                   = {reverse_signed_b(output)}{output} != {input_number['output']}({signed_b(input_number['output'], bit_len*2)})")

        # show process
        _show_process_counter += 1
        _current_percentage = round(_show_process_counter/input_len*100)
        if _current_percentage > _precentage_process:
            _precentage_process = _current_percentage
            print(f"[{_current_percentage:03}%]")


        for lay in range(bit_len-1):
            for index in range(bit_len):
                T0 = mp.gfa[lay][index].tgate[0].p0.gate
                T0p = mp.gfa[lay][index].tgate[0].p1.gate
                T1 = mp.gfa[lay][index].tgate[1].p0.gate
                T1p = mp.gfa[lay][index].tgate[1].p1.gate
                T2 = mp.gfa[lay][index].tgate[2].p0.gate
                T2p = mp.gfa[lay][index].tgate[2].p1.gate

                if T0 == L:
                    stress_counter[lay][index]['T0'] += 1
                if T0p == L:
                    stress_counter[lay][index]['T0p'] += 1
                if T1 == L:
                    stress_counter[lay][index]['T1'] += 1
                if T1p == L:
                    stress_counter[lay][index]['T1p'] += 1
                if T2 == L:
                    stress_counter[lay][index]['T2'] += 1
                if T2p == L:
                    stress_counter[lay][index]['T2p'] += 1


    for lay in range(bit_len-1):
        log.println(f"{[[i/input_len for i in stress.values()] for stress in stress_counter[lay]]}, ")
        for index in range(bit_len):
            stress = stress_counter[lay][index]
            # log.println(f"FA[{lay}][{index}]: {stress}/{input_len} {[i/input_len for i in stress.values()]}")




    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.2f} seconds")
