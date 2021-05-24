import json
import numpy as np
import pandas as pd
import pandapower as pp

from zerobnl.kernel import Node


class Grid(Node):
    def __init__(self):
        super().__init__()

        self.net = pp.create_empty_network()

        for i in ["bus", "bus_geodata", "line", "switch", "trafo", "ext_grid", "load"]:
            df = pd.DataFrame(json.load(open('{}.json'.format(i))))
            df.index = map(int, df.index)
            setattr(self.net, i, df)
			
        print( 'successfully initialized grid' ) 

    def set_attribute(self, attr, value):
        super().set_attribute(attr, value)
        table, name, col = attr.split("/")
        idx = pp.get_element_index(self.net, table, name)
        df = getattr(self.net, table)
        df.loc[idx, col] = value
        #print('set',idx)
        #print('set',col)	
        #print('set',value)


    def get_attribute(self, attr):
        super().get_attribute(attr)
        table, name, col = attr.split("/")
        idx = pp.get_element_index(self.net, table, name)
        df = getattr(self.net, "res_"+table)
        #print('get',idx)
        #print('get',col)		

        return df.loc[idx, col]

    def step(self, value):
        super().step(value)
        pp.runpp(self.net, numba=False)
        print(self.simu_time)
        for key in ["ext_grid/Slack_SK/p_mw", "ext_grid/Slack_SK/q_mvar"]:
            self.save_attribute(key)
            #print('step',key)
            #print('step',value)


if __name__ == "__main__":
    node = Grid()
    node.run()
