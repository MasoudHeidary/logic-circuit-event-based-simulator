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
    
    @property
    def valid(self):
        return [self.H, self.L]
    
    def get_valid(self, lst):
        return [i for i in lst if i in self.valid]
    
    def all(self, data):
        if self.X in data:
            return self.X
        
        _data = self.get_valid(data)
        if len(_data) == 0:
            return self.N
        return self.H if all(_data) else self.L
    
    def any(self, data):
        if self.X in data:
            return self.X
        
        _data = self.get_valid(data)
        if len(_data) == 0:
            return self.N
        return self.H if any(_data) else self.L
    
    def all_same(self, lst):
        return all(elem == lst[0] for elem in lst)
    
V = _v()


# signal (voltage, time)
class Signal:
    def __init__(self, v = V.X, t=0) -> None:
        self.t = t
        self.v = v

    def __eq__(self, obj) -> bool:
        if ((self.t == obj.t) and (self.v == obj.v)):
            return True
        return False
    
    def __repr__(self) -> str:
        return str({'t': self.t, 'v': self.v})
    
    def copy(self) -> object:
        return Signal(self.v, self.t)
    

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


if __name__ == "__main__":
    pass