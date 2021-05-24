import json

from zerobnl.kernel import Node

import numpy as np


class Tes(Node): 
    def __init__(self):
        super().__init__() # Keep this line, it triggers the parent class __init__ method.

        #Inputs (set)
        self.TES_mdot_in = 0.

        #Outputs (get)
        self.TES_SoC = -1.
        self.TES_Qstored = 0.
        self.TES_Qmove = 0.
		
        #Internal variables
        self.cp = 4.186
        self.mm_tes	= 0.0
        self.TES_QstoredMAX = self.parameters['TES_QstoredMAX']
        self.TES_QstoredMIN = self.parameters['TES_QstoredMIN']

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

        if self.TES_mdot_in < 0.:
		
            deltaT = 35.# Assuming a fixed deltaT temporarly
			
        else:
		
            deltaT = 25.# Assuming a fixed deltaT temporarly
		
        self.TES_Qmove = self.TES_mdot_in * self.cp * deltaT
		
        if self.mm_tes < 0.5: # Iteration 1

            #print('Iteration 1')
			
            TES_Qstored_temp = self.TES_Qstored + self.TES_Qmove 
			
            if self.TES_Qstored >= self.TES_QstoredMAX: # TES full		
		
                TES_SoC_temp = 1.
			
            elif self.TES_Qstored <= self.TES_QstoredMIN: # TES empty
		
                TES_SoC_temp = -1.
				
            else:

                TES_SoC_temp = self.TES_SoC 

            self.mm_tes = self.mm_tes + 1	

        else: # Iteration 2
		
            #print('Iteration 2')
			
            self.TES_Qstored = self.TES_Qstored + self.TES_Qmove	
			
            if self.TES_Qstored >= self.TES_QstoredMAX: # TES charge
			
                self.TES_SoC = 1.
			
            elif self.TES_Qstored <= self.TES_QstoredMIN: # TES discharge
		
                self.TES_SoC = -1.
		
            else: # 		
			
                self.TES_SoC = self.TES_SoC	
			       
            self.mm_tes = 0.0		
		
if __name__ == "__main__":
    node = Tes()
    node.run()
