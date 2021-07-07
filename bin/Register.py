# -*- coding: utf-8 -*-
import pandas as pd

class Register:
    def __init__(self):
        
        self.AllZeroType = []
        self.AllZeroT = []
        self.AllZeroV = []
        self.AllBuysT = []
        self.AllBuysV = []
        self.AllSellsT = []
        self.AllSellsV = []

        self.AllProfits =[]
        self.AllWallets = []
        self.AllStockWallets = []
        
        self.TradesT = 0
        self.TotalG = 0
        
    def Register(self, ZeroT, ZeroV, ZeroType, BuysT, SellsT, BuysV, SellsV, Profits, Wallets, StockWallets, Trades, Total):
        self.AllZeroT.append(ZeroT)
        self.AllZeroV.append(ZeroV)
        self.AllZeroType.append(ZeroType)
        self.AllBuysT.append(BuysT)
        self.AllSellsT.append(SellsT)
        self.AllBuysV.append(BuysV)
        self.AllSellsV.append(SellsV)
        self.AllProfits.append(Profits)
        self.AllWallets.append(Wallets)
        self.AllStockWallets.append(StockWallets)
        
        self.TradesT += Trades
        self.TotalG += Total
        
    def Export(self):  
        pass