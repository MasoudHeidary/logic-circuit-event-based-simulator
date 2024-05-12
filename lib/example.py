# import csim
# sim = csim.Simulator()

# generating the input pattern
# def input_pattern():
#     in_pattern = csim.Pattern()
#     in_pattern.v = 0
#     in_pattern.delay(10)
#     in_pattern.v = 1
#     in_pattern.delay(10)
#     in_pattern.delay(10)
#     in_pattern.delay(10)
#     in_pattern.v = 0
#     in_pattern.delay(10)
#     in_pattern.delay(10)

#     return in_pattern.get_data()
# input_pattern = input_pattern()

# def circuit(input):
#     not_gate = csim.Not(pd=10)
#     not_gate.input = input
#     return [not_gate.output]



# output = sim.run(circuit, input_pattern)


# sim.plot(
#     signal=[input_pattern, output],
#     label=["input, not output"]
# )

# print("DONE")


from csim import Plot
from csig import DSignal
from cbasicgate import And


# input pattern
A = DSignal()
B = DSignal()

A.L()
B.L()
A.delay(100)
B.delay(100)

A.L()
B.H()
A.delay(100)
B.delay(100)

A.H()
B.H()
A.delay(100)
B.delay(100)

A.H()
B.L()
A.delay(100)
B.delay(100)




def circuit(A, B):
    return And(IN=[A, B], in_len=2).OUT
def circuit2(A, B):
    return And(IN=[A, B], in_len=2, tpd=10).OUT

cir1_output = [circuit(i, j) for i, j in zip(A.get_data(), B.get_data())]
cir2_output = [circuit2(i, j) for i, j in zip(A.get_data(), B.get_data())]


print(A.get_data())
print(B.get_data())
print(cir1_output)

Plot().plot(signal=[A.get_data(), B.get_data(), cir1_output, cir2_output],
label=['A', 'B', 'And', 'And(with delay)'])

