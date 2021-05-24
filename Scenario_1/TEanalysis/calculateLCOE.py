import numpy as np
# LCOH

class LCOH:
    """
    A class for a LCOH calculation
    """
    def __init__(self,ir,n,start):
	
        self.ir = ir
        self.n = n		
        self.start = start
	
    def	step(self,CAPEXtot,OPEXtot,energy):
	
        d = np.power((1+self.ir),-np.arange(1,self.n+1,1));

        LCOHnum_y1_capex = (CAPEXtot)*d[self.start]; # kr/MWh
        LCOHnum_y1_opex = (OPEXtot)*d[self.start]; # kr/MWh
        LCOHnum_y1 = LCOHnum_y1_capex + LCOHnum_y1_opex;

        LCOHden_y1 = energy*d[self.start]; # MWh

        LCOHnum_op = []
        LCOHden_op = []
        for jj in np.arange(self.start,self.n,1):
            LCOHnum_op.append((OPEXtot)*d[jj])
            LCOHden_op.append(energy*d[jj]); # kr/MWh	

        LCOH_num = LCOHnum_y1+sum(LCOHnum_op);
        LCOH_den = LCOHden_y1+sum(LCOHden_op);
        LCOH_life = LCOH_num / LCOH_den; # kr/MWh

        LCOH_capex = LCOHnum_y1_capex/LCOH_den;
        LCOH_opex = (LCOHnum_y1_opex +sum(LCOHnum_op))/LCOH_den;	
		
        return (LCOH_life, LCOH_capex, LCOH_opex)
