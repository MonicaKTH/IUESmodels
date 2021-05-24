import json

from zerobnl.kernel import Node

import numpy as np


class Hp(Node): 
    def __init__(self):
        super().__init__() # Keep this line, it triggers the parent class __init__ method.

        #Inputs (set)
        self.HP_Ts_rad = 65. # Normally Toutdoor dependent
        self.HP_Tr_rad = 35. # coming from Ctrl_Building
        self.HP_Tin_source = 15. # At some point you might want to consider the return to the ground  -->mdot and variable Tin?

        #Outputs (get)
        self.HP_COP_real = 5.
        self.HP_Pel = 10. # kW
        self.HP_Qth = 0. # kW
		
        #Internal variables
        self.cp = 4.186 # kJ/kg/K
        self.phi = 0.45 # From Heat_Pump_Implementation_Scenarios
        self.B = 10. # From Heat_Pump_Implementation_Scenarios
        self.Tout_source = 10. # At some point you might want to consider the return to the ground  -->mdot and variable Tin?
        self.mdot_n = self.parameters['HP_mdot_hp']
		
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

        if self.HP_Tr_rad > 0:
		
            self.HP_Qth = self.mdot_n * self.cp * (self.HP_Ts_rad - self.HP_Tr_rad)

            self.Tsink = (self.HP_Ts_rad - self.HP_Tr_rad) / 2.

            self.Tsource = (self.HP_Tin_source - self.Tout_source) / 2.

            self.HP_COP_real = self.phi * (self.Tsink + 273.) /(self.Tsink - self.Tsource + self.B) # Temperatures should be in K

            self.HP_Pel = self.HP_Qth / self.HP_COP_real  # kW
			
        else:
		
            self.HP_Qth = 0.		
            self.HP_Pel = self.HP_Qth  # kW       
		
		
if __name__ == "__main__":
    node = Hp()
    node.run()
