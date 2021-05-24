import json

from zerobnl.kernel import Node

import numpy as np


class Ctrl(Node): 
    def __init__(self):
        super().__init__() # Keep this line, it triggers the parent class __init__ method.

        #Inputs (set)
        self.CTRL_Qdem = 61.# Variable coming from the building substation
        self.CTRL_Ts_set = 65. # Normally Toutdoor dependent
        self.CTRL_TesSoC = 1. # feedback from the TES
        #self.CTRL_GridS_trafo = 10 # % Signal of loading from the corresponding transformer
        self.CTRL_Tapt = 20. # feedback from the room		
		
        #Outputs (get)
        self.CTRL_Tr_hp = 35.
        self.CTRL_mdot_tes = 0.
        self.CTRL_signal_EB = 0.
        self.CTRL_signal_DH = 0.
        self.CTRL_Tts = 20.
        self.CTRL_Qth_spilled = 0.

        #Internal variables
        self.cp = 4.186 # kJ/kg/K
        self.mm_c	= 0.0	# Iterations stepper
        self.CTRL_Qdem_it1 = self.CTRL_Qdem
		
        #Parameters
        self.Tr_min = self.parameters['CTRL_Tr_min']
        self.Tr_max = self.parameters['CTRL_Tr_max']
        self.CTRL_mdot_hp = self.parameters['CTRL_mdot_hp']	
        self.CTRL_slines = self.parameters['CTRL_slines']	

        for sline in self.CTRL_slines:
	
            #xx = "CTRL_lineSg_{}".format(sline)
            #xx_value = 0.  # MW
            #exec("%s = %d" % (xx,xx_value))
            self.set_attribute("CTRL_lineSg_{}".format(sline), 0.)	


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

######## Iteration 1
        if self.mm_c < 0.5: 
		
            self.CTRL_Qdem_it1 = self.CTRL_Qdem

			#### To the room ####
            self.CTRL_Tts = 20.

			#### To the supply ####			
            Tr = 65. - self.CTRL_Qdem / (self.cp * self.CTRL_mdot_hp) # Return T if I would use only the HP
								
            self.CTRL_signal_EB = 0. # By default the EB is not used
			
            self.CTRL_signal_DH = 0.	# I assume that the DH is not needed at the first iteration, since EB is an infinite source	
			
            self.CTRL_Qth_spilled = 0.

			# If you do not change mdot, it is like you iterate when the Tr is out of the Tr range.
			# You are assuming perfect prediction, so you are able to control the supply mix accordingly.

            if Tr < self.Tr_min: # The Tret from the B is low, which means that the HP alone is not enough
			
                ## HP
                self.CTRL_Tr_hp = self.Tr_min
	
                mdot = self.CTRL_Qdem / (self.cp * (self.CTRL_Ts_set - self.CTRL_Tr_hp))
	            
				## TES and EB
                if self.CTRL_TesSoC > 0.: # TES is available for discharge (self.TesSoC = 1) 
				
                    self.CTRL_mdot_tes = -(mdot - self.CTRL_mdot_hp) # Discharge is a negative signal. Here insert an if to already check the SoC of the TES
					
                else: # TES is discharged (self.TesSoC = -1) 
				
                    self.CTRL_mdot_tes = 0.    
					
                    self.CTRL_signal_EB = mdot - self.CTRL_mdot_hp # > 0

            elif Tr > self.Tr_max: # The Tret from the B is high, which means that the HP alone is generating too much compared to the B demand

                ## HP
                self.CTRL_Tr_hp = self.Tr_max
	
                mdot = self.CTRL_Qdem / (self.cp * (self.CTRL_Ts_set - self.CTRL_Tr_hp))
				
				## TES
                if self.CTRL_TesSoC < 0.: # TES is available for charge (self.TesSoC = -1) 
				
                    self.CTRL_mdot_tes = self.CTRL_mdot_hp - mdot  # Here insert an if to already check the SoC of the TES					
				
                else: # TES is charged (self.TesSoC = 1) 
				
                    self.CTRL_mdot_tes = 0.  

                    self.CTRL_Qth_spilled = (self.CTRL_mdot_hp - mdot)* self.cp * (25) # Spilled heat !! 	

            else: # The Tret is within the rated range

                ## HP

                self.CTRL_Tr_hp = Tr
	
                mdot = self.CTRL_mdot_hp
	
                self.CTRL_mdot_tes = 0.
				
			#### Iterations stepper ####			
            self.mm_c = self.mm_c + 1 	

######## Iteration 2
        else:
		
            flag = 0		
            for sline in self.CTRL_slines:	
			
                if self.get_attribute("CTRL_lineSg_{}".format(sline)) < 100:
				
                    flag = flag + 0
					
                else:						
                    flag = flag + 1		
 			
			
            if flag < 1: # The grid is not overloaded
			
                #print('Grid ok')
				
                self.CTRL_Tr_hp = self.CTRL_Tr_hp	

            else: # The grid is overloaded		

			#### To the room ####
			
			    # In some scenarios I will consider to lower the thermostat setpoint 
			
			#### To the supply ####
			
				# Grid overloaded: NO HP NOR EB
                self.CTRL_Tr_hp = -1	
                self.CTRL_signal_EB = 0.
                self.CTRL_Qth_spilled = 0.
				
				## TES and DH				
                if self.CTRL_TesSoC > 0: # TES is available for discharge (self.TesSoC = 1) 
				
                    self.CTRL_mdot_tes = -self.CTRL_Qdem_it1 / (self.cp * 35) # Discharge is a negative signal.
					#This mass flow will depend on how I am going to size the TES. Here I am assuming a deltaT of 30 Cdeg
					
                    self.CTRL_signal_DH = 0.                    
					
                else: # TES is discharged (self.TesSoC = -1) 
				
                    self.CTRL_mdot_tes = 0. 
					
                    self.CTRL_signal_DH = self.CTRL_Qdem_it1
			       
			#### Iterations stepper ####
            self.mm_c = 0.0 	
				
if __name__ == "__main__":
    node = Ctrl()
    node.run()
