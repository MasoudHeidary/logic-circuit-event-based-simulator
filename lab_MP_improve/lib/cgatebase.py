from .csig import *


class GateBase:
    def __init__(self) -> None:
        
        self.__old_data = None
    
    @property
    def data_list(self):
        return []

    @property
    def change_flag(self):
        new_data = self.data_list
        if (new_data == self.__old_data):
            return False
        # self.__old_data = new_data.copy()     # don't change the flag, just checking the flag
        return True
    
    def update_flag(self):
        new_data = self.data_list
        self.__old_data = new_data

    def run(self):
        while self.change_flag:
            self.update_flag()
            self.netlist()

    def netlist(self):
        pass

class Gate(GateBase):
    def __init__(self) -> None:
        super().__init__()
        self.__old_data = None

    @property
    def element_list(self):
        return []

    @property
    def change_flag(self):
        new_data = self.data_list
        if(new_data != self.__old_data):
            self.__old_data = new_data.copy()
            return True
        
        flag_lst = [i.change_flag for i in self.element_list]
        if(any(flag_lst)):
            return True
        return False
            