# -*- coding: utf-8 -*-
import numpy as np

class Optimizer:
    def __init__(self):
        self.active = True
        
    def Mean1D(self, Listx, Listy):
        
        DataArray = np.asanyarray(Listy)
        NewListy = np.nanmean(DataArray, axis=0)
        
        if len(NewListy) == len(Listx[0]):
            return Listx[0], list(NewListy)
        
        else:
            print("NO GOD! PLEASE NO!!! NOOOOOOOOOO")
    
    def Med1D(self, Listx, Listy):
        
        YArray = np.asanyarray(Listy)
        NewListy = np.nanmedian(YArray, axis=0)
        
        if len(NewListy) == len(Listx[0]):
            return Listx[0], list(NewListy)
        
        else:
            print("NO GOD! PLEASE NO!!! NOOOOOOOOOO")