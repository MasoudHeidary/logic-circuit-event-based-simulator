from Multiplier import *

def counter(ll):
    count_dict = {}

    for i in ll:
        if str(i) in count_dict:
            count_dict[str(i)] += 1
        else:
            count_dict[str(i)] = 1
        
    return count_dict


input_patterns = []
output_patterns = []
for A in range(0xF+1):
    for B in range(0xF+1):
        def _(num: int, length: int = 4):
            return list(map(int, reversed(format(num, f'0{length}b'))))
        input_patterns += [{'A': _(A), 'B': _(B)}]
        output_patterns += [_(A*B, 8)]


# find the most common pattern in the last FA in critical path
gnum = 1    # gate number
output = []
for i in range(len(input_patterns)):
    # mp4 = MP4()
    mp4 = MP4_manipulated()

    mp4.A = input_patterns[i]['A']
    mp4.B = input_patterns[i]['B'] 

    mp4.output

    # print(mp4.gfa[gnum].sum, mp4.gfa[gnum].carry)
    # output += [[mp4.gfa[gnum].A, mp4.gfa[gnum].B, mp4.gfa[gnum].C]]
    print(f"{mp4.A}, {mp4.B}, => {mp4.output}, {mp4.output == output_patterns[i]}")
    output += [[mp4.gfa[gnum].A, mp4.gfa[gnum].B, mp4.gfa[gnum].C]]
print(counter(output))