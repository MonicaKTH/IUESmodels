import json

from zerobnl.kernel import Node

import numpy as np


class Hsub(Node): 
    def __init__(self):
        super().__init__() # Keep this line, it triggers the parent class __init__ method.

        #Inputs (set)
        self.HSUB_Qdem_unit = 0.6
        #Outputs (get)
        self.HSUB_Qdem_B = 0.6 * 101.
		
        #Internal variables
        self.m2unit = 48. # m2
        self.HSUB_m2B = self.parameters['HSUB_m2B'] # m2
		
    def set_attribute(self, attr, value):
        """This method is called to set an attribute of the model to a given value, you need to adapt it to your model."""
        super().set_attribute(attr, value)  # Keep this line, it triggers the parent class method.
        setattr(self, attr, value)

    def get_attribute(self, attr):
        """This method is called to get the value of an attribute, you need to adapt it to your model."""
        super().get_attribute(attr)  # Keep this line, it triggers the parent class method.
        return getattr(self, attr)

    def step(self, value):
        """This method is called to make a step, you need to adapt it to your model."""
        super().step(value)  # Keep this line, it triggers the parent class method.

        self.scale = self.HSUB_m2B / self.m2unit       

        self.HSUB_Qdem_B = self.HSUB_Qdem_unit * self.scale / 1000. # kW
		
		
if __name__ == "__main__":
    node = Hsub()
    node.run()
