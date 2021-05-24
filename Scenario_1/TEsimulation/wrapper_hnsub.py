import json

from zerobnl.kernel import Node

import numpy as np


class Hnsub(Node): 
    def __init__(self):
        super().__init__() # Keep this line, it triggers the parent class __init__ method.

        #Inputs (set)
        self.DHSUB_Qth = 10. # kW
        #Outputs (get)		
        #Parameters
        self.DHSUB_m2B = self.parameters['DHSUB_m2B'] # m2
        self.DHSUB_m2B_ref = self.parameters['DHSUB_m2B_ref'] # m2
		
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

        self.DHSUB_Qth_unit = self.DHSUB_Qth / self.DHSUB_m2B_ref  # MW
		
        ii = 0
		
        self.DHSUB_Qth_unitB1 = self.DHSUB_Qth_unit * self.DHSUB_m2B[ii]
		
        self.DHSUB_Qth_unitB2 = self.DHSUB_Qth_unit * self.DHSUB_m2B[ii+1]
		
        self.DHSUB_Qth_unitB3 = self.DHSUB_Qth_unit * self.DHSUB_m2B[ii+2]
		
        self.DHSUB_Qth_unitB4 = self.DHSUB_Qth_unit * self.DHSUB_m2B[ii+3]
		
        self.DHSUB_Qth_unitB5 = self.DHSUB_Qth_unit * self.DHSUB_m2B[ii+4]
		
        self.DHSUB_Qth_unitB6 = self.DHSUB_Qth_unit * self.DHSUB_m2B[ii+5]
		
        self.DHSUB_Qth_unitB7 = self.DHSUB_Qth_unit * self.DHSUB_m2B[ii+6]
 		
        self.DHSUB_Qth_unitB8 = self.DHSUB_Qth_unit * self.DHSUB_m2B[ii+7]
		
        self.DHSUB_Qth_unitB9 = self.DHSUB_Qth_unit * self.DHSUB_m2B[ii+8]
		
        self.DHSUB_Qth_unitB10 = self.DHSUB_Qth_unit * self.DHSUB_m2B[ii+9]
		
        self.DHSUB_Qth_unitB11 = self.DHSUB_Qth_unit * self.DHSUB_m2B[ii+10]
		
        self.DHSUB_Qth_unitB12 = self.DHSUB_Qth_unit * self.DHSUB_m2B[ii+11]
		
        self.DHSUB_Qth_unitB13 = self.DHSUB_Qth_unit * self.DHSUB_m2B[ii+12]
		
        self.DHSUB_Qth_unitB14 = self.DHSUB_Qth_unit * self.DHSUB_m2B[ii+13]
		
        self.DHSUB_Qth_unitB15 = self.DHSUB_Qth_unit * self.DHSUB_m2B[ii+14]
		
        self.DHSUB_Qth_unitB16 = self.DHSUB_Qth_unit * self.DHSUB_m2B[ii+15]
		
        self.DHSUB_Qth_unitB17 = self.DHSUB_Qth_unit * self.DHSUB_m2B[ii+16]
		
        self.DHSUB_Qth_unitB18 = self.DHSUB_Qth_unit * self.DHSUB_m2B[ii+17]
		
        self.DHSUB_Qth_unitB19 = self.DHSUB_Qth_unit * self.DHSUB_m2B[ii+18]
		
        self.DHSUB_Qth_unitB20 = self.DHSUB_Qth_unit * self.DHSUB_m2B[ii+19]
		
        self.DHSUB_Qth_unitB21 = self.DHSUB_Qth_unit * self.DHSUB_m2B[ii+20]
		
        self.DHSUB_Qth_unitB22 = self.DHSUB_Qth_unit * self.DHSUB_m2B[ii+21]
		
if __name__ == "__main__":
    node = Hnsub()
    node.run()
