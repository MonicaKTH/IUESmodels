import json
import pandas as pd

from zerobnl.kernel import Node

class Dh(Node): 
    def __init__(self):
        super().__init__() # Keep this line, it triggers the parent class __init__ method.

        #Inputs (set)

		
        #Outputs (get)
        self.DH_PE = 0.
		
        # Parameters
		
        for i in ["loads"]:
            self.dhn = pd.read_csv('DHN_{}.csv'.format(i),sep=';')
			
        #Internal variables
		
        print( 'successfully initialized dh' ) 

    def set_attribute(self, attr, value):
        """This method is called to set an attribute of the model to a given value, you need to adapt it to your model."""
        super().set_attribute(attr, value)  # Keep this line, it triggers the parent class method.
        #setattr(self, attr, value)
		
        idx = self.dhn[self.dhn['name']==attr].index.tolist() 
        self.dhn.loc[idx, 'q_kw'] = value

    def get_attribute(self, attr):
        """This method is called to get the value of an attribute, you need to adapt it to your model."""
        super().get_attribute(attr)  # Keep this line, it triggers the parent class method.
        return getattr(self, attr)
		
        # Nothing relevant is happening, since the model is just a summation

    def step(self, value):
        """This method is called to make a step, you need to adapt it to your model."""
        super().step(value)  # Keep this line, it triggers the parent class method.		
	
        self.DH_PE = sum(self.dhn['q_kw'])		
		
if __name__ == "__main__":
    node = Dh()
    node.run()
