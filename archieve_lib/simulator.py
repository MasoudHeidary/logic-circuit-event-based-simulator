from Multiplier import *


# we try to add timing to our system to make the simulation real
# capture the changes and maybe plot the output

# (time, value)

class simulator:

    def __init__(self) -> None:
        self.n = Not()
        self.output = []
        self.clk = N
        self.time = 0
        pass

    def run(self):
        self.delay(0)
        self.bench()
        self.delay(0)


    
    def netlist(self):
        self.n.input = self.clk
        self.n.output
    
    def run_netlist(self):
        self.netlist()
        while self.n.change_flag:
            self.netlist()

    def delay(self, t):
        self.save()
        self.time += t

    def save(self):
        self.run_netlist()
        self.output += [
            {'time': self.time, 'clk': self.clk, 'output': self.n.output}
        ]


    def bench(self):

        self.clk = L
        self.delay(10)

        self.clk = H
        self.delay(10)








sim = simulator()
sim.run()
print(sim.output)
