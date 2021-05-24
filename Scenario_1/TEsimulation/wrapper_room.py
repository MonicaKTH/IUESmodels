import json

from zerobnl.kernel import Node

import numpy as np
import fmipp
import os.path


class MyNode(Node):
    """docstring for MyNode"""

    def __init__(self):
        super().__init__()  # Keep this line, it triggers the parent class __init__ method.

        # This is where you define the attribute of your model, this one is pretty basic.
        # FMU loading
		
        work_dir = os.path.split(os.path.abspath(__file__))[0]  # define working directory
        fmu_name = self.parameters['ROOM_FMUname']  # define FMU model name
        path_to_fmu = os.path.join(work_dir, fmu_name)  # path to FMU		
        uri_to_extracted_fmu = fmipp.extractFMU(path_to_fmu, work_dir)  # extract FMU	
        logging_on = False
        time_diff_resolution = 1e-9	
        model_name = fmu_name.replace('.fmu', '')		
        self.fmu = fmipp.RollbackFMU(uri_to_extracted_fmu, model_name, logging_on, time_diff_resolution)
        #print( 'successfully loaded the FMU' )
		
        ## FMU instantiation
        start_time = 0.
        #stop_time = 3600.* 168.  # 24 hours
        self.step_size = 3600.# 450. # 1 hour
        self.tempo = start_time
        instance_name = "modelica_fmu_test"
        #visible = False
        #interactive = False
        status = self.fmu.instantiate(instance_name)
        assert status == fmipp.fmiOK        
        #print( 'successfully instantiated the FMU' )
		
        self.fmu.setRealValue('setTemp', 20.)		

        ## FMU initialization
        #stop_time_defined = True
        status = self.fmu.initialize()
        assert status == fmipp.fmiOK        
        #print( 'successfully initialized the FMU' ) 

        self.mm	= 0.0	
        self.temponew = (self.tempo + self.step_size)

    def set_attribute(self, attr, value):
        """This method is called to set an attribute of the model to a given value, you need to adapt it to your model."""
        super().set_attribute(attr, value)  # Keep this line, it triggers the parent class method.

        self.fmu.setRealValue(attr, value)
        assert self.fmu.getLastStatus() == fmipp.fmiOK  

    def get_attribute(self, attr):
        """This method is called to get the value of an attribute, you need to adapt it to your model."""
        super().get_attribute(attr)  # Keep this line, it triggers the parent class method.
		
        output1 = self.fmu.getRealValue(attr) 

        #print('outputs', output1)
 
        return output1

    def step(self, value):
        """This method is called to make a step, you need to adapt it to your model."""
        super().step(value)  # Keep this line, it triggers the parent class method.

        if self.mm < 0.5:
		
            # Make integration step: 1h	

            self.temponew = self.fmu.integrate(self.tempo + self.step_size)     			
			
            #print('model tempo it 1 in',self.tempo)	
            #print('model tempo it 1 out',self.temponew)

            #print('real tempo it 1',self.real_time)
            #print('simu tempo it 1',self.simu_time)	

            self.mm = self.mm + 1	

        else:
		
            if self.temponew < (self.tempo + self.step_size):		

                self.tempo =  self.tempo + self.step_size
			
            else:

                status2 = self.fmu.integrate(self.tempo)			
			
                self.tempo = self.fmu.integrate(self.tempo + self.step_size)
			
                #print('model tempo it 2 back',status2)			
                #print('model tempo it 2 out',self.tempo)		

                #print('real tempo it 2',self.real_time)
                #print('simu tempo it 2',self.simu_time)	
			       
            self.mm = 0.0

if __name__ == "__main__":
    node = MyNode()
    node.run()