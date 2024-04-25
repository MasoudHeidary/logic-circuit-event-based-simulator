import csim
sim = csim.Simulator()


in_pattern = [
    csim.Signal(0, csim.L),
    csim.Signal(10, csim.H),
    csim.Signal(20, csim.H),
    csim.Signal(30, csim.H),
    csim.Signal(40, csim.L),
    csim.Signal(50, csim.L),
]

def circuit(input):
    not_gate = csim.Not(pd=10)
    not_gate.input = input
    return [not_gate.output]



sim.input_pattern = in_pattern
output = sim.run(circuit)

# print(output)

# sim.plot(sim.input_pattern, "input")
# sim.plot(sim.output_pattern, "Not Output")
# sim.show_plot()

sim.plot(
    signal=[in_pattern, output],
    label=["input, not output"]
)
