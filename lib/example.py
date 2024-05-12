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


from csim import Plot, DynamicSimulator
from cbasicgate import And, DSignal, Signal, V


A = Signal()
B = Signal()
gand = And(IN=[A, B], in_len=2)

input_data = DynamicSimulator(sig_list=[A, B])
output_data = DynamicSimulator()
# input_data.save()
# output_data.save(gand.OUT)


A.H()
B.H()
A.delay(10)
B.delay(10)
input_data.save()
output_data.save(gand.OUT)


A.H()
B.L()
A.delay(10)
B.delay(10)
input_data.save()
output_data.save(gand.OUT)


Plot().plot(signal=[input_data.get_data()[0], input_data.get_data()[1], output_data.get_data()])


exit()

A = Signal()
B = Signal()
gand = And(IN=[A, B], in_len=2)

A.H()
B.H()
print(gand.OUT)

exit()

dsig = DSignal()
A = []
pA = []
B = []
pB = []
out = []

A = dsig.L
pA += [A]
B = dsig.L
pB += [B]
out.append(And([A, B], tpd=10).OUT)
dsig.delay(50)

A = dsig.L
pA += [A]
B = dsig.H
pB += [B]
out.append(And([A, B], tpd=10).OUT)
dsig.delay(50)

A = dsig.H
pA += [A]
B = dsig.L
pB += [B]
out.append(And([A, B], tpd=10).OUT)
dsig.delay(50)

A = dsig.H
pA += [A]
B = dsig.H
pB += [B]
out.append(And([A, B], tpd=10).OUT)
dsig.delay(50)

pA += [dsig.H]


Plot().plot(signal=[pA, pB, out], label=['A', 'B', 'output'])
