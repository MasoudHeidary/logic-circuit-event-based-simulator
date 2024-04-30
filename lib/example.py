import csim
sim = csim.Simulator()


# generating the input pattern
def input_pattern():
    in_pattern = csim.Pattern()
    in_pattern.v = 0
    in_pattern.delay(10)
    in_pattern.v = 1
    in_pattern.delay(10)
    in_pattern.delay(10)
    in_pattern.delay(10)
    in_pattern.v = 0
    in_pattern.delay(10)
    in_pattern.delay(10)

    return in_pattern.get_data()
input_pattern = input_pattern()

def circuit(input):
    not_gate = csim.Not(pd=10)
    not_gate.input = input
    return [not_gate.output]



output = sim.run(circuit, input_pattern)


sim.plot(
    signal=[input_pattern, output],
    label=["input, not output"]
)

print("DONE")
