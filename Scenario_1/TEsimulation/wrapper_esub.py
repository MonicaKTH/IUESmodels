import json

from zerobnl.kernel import Node

import numpy as np


class Esub(Node): 
    def __init__(self):
        super().__init__() # Keep this line, it triggers the parent class __init__ method.

        #Inputs (set)
        self.ESUB_Pel_hp = 0. # kW
        self.ESUB_Pel_eb = 0. # kW
        self.ESUB_Pel_ea = 0. # kW
        #Outputs (get)	

        self.ESUB_cpoints = self.parameters['ESUB_cpoints']
        self.ESUB_cpointsALL = self.parameters['ESUB_cpointsALL']
		
        for cpoint in self.ESUB_cpointsALL:
		
            #xx = "ESUB_Pel_{}".format(cpoint)
            #yy = "ESUB_Qel_{}".format(cpoint)

            #xx_value = 0.  # MW
            #yy_value = 0.
            #exec("%s = %d" % (xx,xx_value))
            #exec("%s = %d" % (yy,yy_value))	
			
            self.set_attribute("ESUB_Pel_{}".format(cpoint), 0.)
            self.set_attribute("ESUB_Qel_{}".format(cpoint), 0.)
		
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

        #self.ESUB_Pel_B = (self.ESUB_Pel_hp + self.ESUB_Pel_eb+self.ESUB_Pel_ea)/1000.  # MW
        #self.ESUB_Qel_B = self.ESUB_Pel_B * 0.1
		
        self.ESUB_Pel_hp = self.ESUB_Pel_hp / len(self.ESUB_cpoints)
        self.ESUB_Pel_eb = self.ESUB_Pel_eb / len(self.ESUB_cpoints)			
        self.ESUB_Pel_ea = self.ESUB_Pel_ea / len(self.ESUB_cpoints)
        
        for cpoint in self.ESUB_cpoints:
		
            #xx = "ESUB_Pel_{}".format(cpoint)
            #yy = "ESUB_Qel_{}".format(cpoint)

            xx_value = (self.ESUB_Pel_hp + self.ESUB_Pel_eb+self.ESUB_Pel_ea)/1000.  # MW
            yy_value = xx_value * 0.1
            #exec("%s = %d" % (xx,xx_value))
            #exec("%s = %d" % (yy,yy_value))	

            self.set_attribute("ESUB_Pel_{}".format(cpoint), xx_value)
            self.set_attribute("ESUB_Qel_{}".format(cpoint), yy_value)
			
if __name__ == "__main__":
    node = Esub()
    node.run()
