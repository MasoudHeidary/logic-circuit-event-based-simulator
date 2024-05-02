# signals


# voltage control
class _v:
    @property
    def L(self):
        return 0
    @property
    def H(self):
        return 1
    @property
    def X(self):
        return 2
    @property
    def N(self):
        return 3
    
V = _v()


# signal (voltage, time)
class Signal:
    def __init__(self, value = V.X, t=0) -> None:
        self.t = t
        self.value = value

    def __eq__(self, obj) -> bool:
        if ((self.t == obj.t) and (self.value == obj.value)):
            return True
        return False
    
    def __repr__(self) -> str:
        return str({'t': self.t, 'value': self.value})
    
    def copy(self) -> object:
        return Signal(self.t, self.value)
    

# dynamic signal, user friendly
class DSignal:
    def __init__(self) -> None:
        self.t = 0
    
    def delay(self, t):
        self.t += t
    

    @property
    def L(self):
        return Signal(V.L, self.t)
    @property
    def H(self):
        return Signal(V.H, self.t)
    @property
    def X(self):
        return Signal(V.X, self.t)
    @property
    def N(self):
        return Signal(V.N, self.t)

