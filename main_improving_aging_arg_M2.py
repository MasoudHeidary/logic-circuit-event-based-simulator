from concurrent.futures import ProcessPoolExecutor
import time
import log
import sys
from Multiplier import *
import multiprocessing
import os

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

# Function to process a batch of inputs, calculate stress counters, and return results
def process_batch(batch, bit_len, arg_FA_i, arg_FA_j, arg_tgate, arg_p, optimizer_enable, queue):
    stress_counter = [
        [{'T0': 0, 'T0p': 0, 'T1': 0, 'T1p': 0, 'T2': 0, 'T2p': 0} for _ in range(bit_len)] 
        for _ in range(bit_len-1)
    ]

    for A, B in batch:
        mp = MPn_v3(signed_b(A, bit_len), signed_b(B, bit_len), bit_len)
        mp.output

        optimized_flag = False
        if optimizer_enable:
            if (A != -1 * 2**(bit_len - 1)) and (B != -1 * 2**(bit_len - 1)):
                _con = (
                    mp.gfa[arg_FA_i][arg_FA_j].tgate[arg_tgate].p0.gate == L
                ) if (arg_p == 0) else (
                    mp.gfa[arg_FA_i][arg_FA_j].tgate[arg_tgate].p1.gate == L
                )
                if _con:
                    neg_A = -A
                    neg_B = -B
                    neg_mp = MPn_v3(signed_b(neg_A, bit_len), signed_b(neg_B, bit_len), bit_len)
                    neg_mp.output

                    _con_1 = (
                        neg_mp.gfa[arg_FA_i][arg_FA_j].tgate[arg_tgate].p0.gate == H
                    ) if (arg_p == 0) else (
                        neg_mp.gfa[arg_FA_i][arg_FA_j].tgate[arg_tgate].p1.gate == H
                    )
                    if _con_1:
                        mp = neg_mp
                        optimized_flag = True

        output = mp.output
        if output != signed_b(A * B, bit_len * 2):
            raise RuntimeError(f"Multiplier test failed for {A} x {B}. Output: {output} != Expected: {A * B}")

        # Update stress counter for the current A and B
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

    # Put the results in the queue for the main process to aggregate
    queue.put(stress_counter)
    # print(f"Process {os.getpid()}: Completed batch processing")
    return;

# Generator to create batches of inputs
def generate_batches(bit_len, batch_size):
    _range = range(-1 * 2**(bit_len - 1), 2**(bit_len - 1))
    batch = []
    for A in _range:
        for B in _range:
            batch.append((A, B))
            if len(batch) >= batch_size:
                yield batch
                batch = []
    # Yield the last batch if it contains any remaining pairs
    if batch:
        yield batch

# Function to create and manage processes dynamically with batch processing
def process_inputs_in_batches(bit_len, arg_FA_i, arg_FA_j, arg_tgate, arg_p, optimizer_enable, batch_size):
    processes = []
    batch_generator = generate_batches(bit_len, batch_size)
    
    total_stress_counter = [
        [{'T0': 0, 'T0p': 0, 'T1': 0, 'T1p': 0, 'T2': 0, 'T2p': 0} for _ in range(bit_len)] 
        for _ in range(bit_len-1)
    ]

    queue = multiprocessing.Queue(maxsize=100_000_000)

    # batch_count = 0
    p_counter = 0
    for batch in batch_generator:
        # Create a new process for each batch of input pairs
        p = multiprocessing.Process(
            target=process_batch, 
            args=(batch, bit_len, arg_FA_i, arg_FA_j, arg_tgate, arg_p, optimizer_enable, queue)
        )
        processes.append(p)
        p.start()

        # batch_count += 1

        # Limit the number of active processes
        # if len(processes) >= multiprocessing.cpu_count():
        if len(processes) >= 20:
            for p in processes:
                # print("join")
                p.join()  # Wait for each process to finish
                print(f"{p_counter} p DONE")
                p_counter += 1
            while not queue.empty():
                # print("que get")
                stress_counter = queue.get()  # Get the stress results from the queue
                # Aggregate stress counters from each batch
                for lay in range(bit_len - 1):
                    for index in range(bit_len):
                        for key in total_stress_counter[lay][index]:
                            total_stress_counter[lay][index][key] += stress_counter[lay][index][key]
            processes = []  # Clear process list after joining
            # print("cleaning")

    # print("final join")
    # Ensure all processes are finished
    for p in processes:
        p.join()
    
    while not queue.empty():
        stress_counter = queue.get()  # Get the stress results from the queue
        # Aggregate stress counters from each batch
        for lay in range(bit_len - 1):
            for index in range(bit_len):
                for key in total_stress_counter[lay][index]:
                    total_stress_counter[lay][index][key] += stress_counter[lay][index][key]

    # Print the aggregated stress counters
    input_len = (2**bit_len)**2  # Total number of input pairs
    for lay in range(bit_len-1):
        # print(f"Layer {lay}: {[stress for stress in total_stress_counter[lay]]}")
        print(f"{[[i/input_len for i in stress.values()] for stress in total_stress_counter[lay]]}, ")
        # for index in range(bit_len):
            # stress = total_stress_counter[lay][index]
            # print(f"FA[{lay}][{index}]: {stress}/{input_len} {[i/input_len for i in stress.values()]}")
            # print(f"FA[{lay}][{index}]: {stress}/{input_len} {[i/input_len for i in stress.values()]}")

if __name__ == "__main__":
    bit_len = 8
    optimizer_enable = True
    batch_size = 1000 

    arg_FA_i = int(sys.argv[1])
    arg_FA_j = int(sys.argv[2])
    arg_tgate = int(sys.argv[3])
    arg_p = int(sys.argv[4])

    start_time = time.time()

    # Dynamically process inputs in batches and calculate stress counters
    process_inputs_in_batches(bit_len, arg_FA_i, arg_FA_j, arg_tgate, arg_p, optimizer_enable, batch_size)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total execution time: {elapsed_time:.2f} seconds")

