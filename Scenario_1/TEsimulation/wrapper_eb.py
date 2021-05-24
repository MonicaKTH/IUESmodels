import json

from zerobnl.kernel import Node

import numpy as np


class Eb(Node): 
    def __init__(self):
        super().__init__() # Keep this line, it triggers the parent class __init__ method.

        #Inputs (set)
        self.EB_signal = 0.

        #Outputs (get)
        self.EB_Pel = 0.
		
        #Internal variables

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
		


        if self.EB_signal > 0.: # EB on
		
            Qth = self.EB_signal * 4.186 * 35. # For the moment I put a random deltaT, in the future I should have the Tr from the control or the remaining Qdem
            # I have to make sure that the balance is satisfied			
		
            self.EB_Pel = Qth / 0.9 # kW
			
        else: # EB off
		
            self.EB_Pel = 0.
		
      
		
		
if __name__ == "__main__":
    node = Eb()
    node.run()
