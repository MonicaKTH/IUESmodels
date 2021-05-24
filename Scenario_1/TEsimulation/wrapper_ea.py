import json

from zerobnl.kernel import Node

import numpy as np

import pandas as pd


class Ea(Node): 
    def __init__(self):
        super().__init__() # Keep this line, it triggers the parent class __init__ method.

        #Inputs (set)
        self.EA_Pel_unit = pd.read_csv(self.parameters['EA_file'],sep=';')
        #Outputs (get)
        self.EA_Pel = 0.
		
        #Parameters		
        self.EA_m2B = self.parameters['EA_m2B'] # m2
		
        #Internal variables			
        self.mm_ea	= 0.0
        self.Icurve = 1
		
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
		
        if self.mm_ea < 0.5: # Iteration 1

            self.EA_Pel = self.EA_Pel_unit['Pel_ea_m2'][self.Icurve] * self.EA_m2B # kW	

            self.mm_ea = self.mm_ea + 1	

        else: # Iteration 2
		
            self.Icurve = self.Icurve + 1       
            self.mm_ea = 0.0		
		
		
if __name__ == "__main__":
    node = Ea()
    node.run()
