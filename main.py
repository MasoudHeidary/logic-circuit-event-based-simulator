from Multiplier import *

# find number of PMOSes under stress in critical path of a multiplier
# under stress: simple the gate input should be zero(L)


def FA_counter(module: FA):
    counter  = 0
    for ngate in module.ngate:
        ngate: Not
        if(ngate.p.gate == L):
            counter += 1
    
    for tgate in module.tgate:
        tgate: Trans
        if(tgate.p0.gate == L):
            counter += 1
        if(tgate.p1.gate == L):
            counter += 1

    return counter
    
def and_counter(module: And):
    counter = 0
    for pmos in module.p:
        if pmos.gate == L:
            counter += 1
    return counter

def MP4_counter(module: MP4):
    counter = 0
    for and_gate in module.gand:
        counter += and_counter(and_gate)
    for FA_gate in module.gfa:
        counter += FA_counter(FA_gate)
    return counter



"""
counter_list = []
for A in range(0xF + 1):
    for B in range(0xF + 1):
        def _(x):
            return list(map(int, format(x, '04b')))
        
        mp = MP4()
        mp.A = _(A)
        mp.B = _(B)
        mp.output

        counter_list += [MP4_counter(mp)]
        if(MP4_counter(mp) >= 170):
            print(f"{mp.A} * {mp.B} = {mp.output} ### {MP4_counter(mp)}")
        

print(min(counter_list))
print(max(counter_list))
"""



















