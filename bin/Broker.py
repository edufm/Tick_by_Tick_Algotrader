# -*- coding: utf-8 -*-
import numpy as np

class Broker_Standart:
    def __init__(self):
        self.currentbuy  = 0
        self.currentsell  = 0
        self.currentzero = 0
        
        self.profit = 0
        self.stockwallet = 0
        self.wallet = 0
        
        self.ZeroT = []
        self.ZeroV = []
        self.ZeroType = []
        self.BuysT = []
        self.BuysV = []
        self.SellsT = []
        self.SellsV = []
        
        self.Profits =[]
        self.Wallets = []
        self.StockWallets = [] 
        
        self.status = "clear"  

    def Buy(self, bet, askvalue, time, targetvalue):
        self.stockwallet += bet
        self.StockWallets.append(self.stockwallet)
        self.wallet -= bet * askvalue
        self.Wallets.append(self.wallet)
        self.profit = self.wallet + self.stockwallet * askvalue
        self.Profits.append(self.profit)
        self.BuysT.append(time)
        self.BuysV.append(askvalue)
        
    def Sell(self, bet, bidvalue, time, targetvalue):
        self.stockwallet -= bet
        self.StockWallets.append(self.stockwallet)
        self.wallet += bet *bidvalue
        self.Wallets.append(self.wallet)
        self.profit = self.wallet + self.stockwallet * bidvalue
        self.Profits.append(self.profit)
        self.SellsT.append(time)
        self.SellsV.append(bidvalue)
        
    def Zero(self, bet, bidvalue, askvalue, time, targetvalue):
        if self.stockwallet > 0:
            self.ZeroT.append(time)
            self.ZeroV.append(bidvalue)
            self.ZeroType.append("Sell")
            self.wallet += bidvalue * (self.stockwallet)
        elif self.stockwallet < 0:
            self.ZeroT.append(time)
            self.ZeroV.append(askvalue)
            self.ZeroType.append("Buy")
            self.wallet += askvalue * (self.stockwallet)
        self.Wallets.append(self.wallet)
        self.stockwallet = 0
        self.StockWallets.append(self.stockwallet)
        self.profit = self.wallet
        self.Profits.append(self.profit)
        
    def Endseq(self):
    
        value = (self.BuysT[self.currentbuy:len(self.BuysT)], self.BuysV[self.currentbuy:len(self.BuysT)],
                 self.SellsT[self.currentsell:len(self.SellsT)], self.SellsV[self.currentsell:len(self.SellsV)],
                self.ZeroT[self.currentzero:len(self.ZeroT)], self.ZeroV[self.currentzero:len(self.ZeroV)], 
                self.Profits[self.currentzero:len(self.Profits)])

        self.currentbuy = len(self.BuysT)
        self.currentsell = len(self.SellsT)
        self.currentzero = len(self.ZeroT)
        
        return value

    def Endday(self, bet, bidvalue, askvalue, time):
        if self.stockwallet > 0:
            self.ZeroT.append(time)
            self.ZeroV.append(bidvalue)
            self.ZeroType.append("Sell")
            self.wallet += bidvalue * (self.stockwallet)
            self.Wallets.append(self.wallet)
            self.stockwallet = 0
            self.StockWallets.append(self.stockwallet)
            self.profit = self.wallet
            self.Profits.append(self.profit)
        elif self.stockwallet < 0:
            self.ZeroT.append(time)
            self.ZeroV.append(askvalue)
            self.ZeroType.append("Buy")
            self.wallet += askvalue * (self.stockwallet)
            self.Wallets.append(self.wallet)
            self.stockwallet = 0
            self.StockWallets.append(self.stockwallet)
            self.profit = self.wallet
            self.Profits.append(self.profit)
    
    def Reset(self):        
        self.currentbuy  = 0
        self.currentsell  = 0
        self.currentzero = 0
        
        self.profit = 0
        self.stockwallet = 0
        self.wallet = 0
        self.operate = 0
        self.oldsign = np.sign(0)
        self.lastvalue = 0
        
        self.ZeroT = []
        self.ZeroV = []
        self.ZeroType = []
        self.BuysT = []
        self.BuysV = []
        self.SellsT = []
        self.SellsV = []
        
        self.Profits =[]
        self.Wallets = []
        self.StockWallets = [] 
        
class Broker_Waiter:
    def __init__(self):
        self.currentbuy  = 0
        self.currentsell  = 0
        self.currentzero = 0
        
        self.profit = 0
        self.stockwallet = 0
        self.wallet = 0
        
        self.ZeroT = []
        self.ZeroV = []
        self.ZeroType = []
        self.BuysT = []
        self.BuysV = []
        self.SellsT = []
        self.SellsV = []
        
        self.Profits =[]
        self.Wallets = []
        self.StockWallets = [] 
        
        self.status = "clear"   
        self.currentbet = 100
        self.waiting = 0
        

    def Buy(self, bet, askvalue, time, targetvalue):
        if askvalue <= targetvalue:
            self.stockwallet += bet
            self.StockWallets.append(self.stockwallet)
            self.wallet -= bet * askvalue
            self.Wallets.append(self.wallet)
            self.profit = self.wallet + self.stockwallet * askvalue
            self.Profits.append(self.profit)
            self.BuysT.append(time)
            self.BuysV.append(askvalue)
        else:
            self.status = "Buying"
            self.currentbet = bet
        
    def Sell(self, bet, bidvalue, time, targetvalue):
        if bidvalue >= targetvalue:
            self.stockwallet -= bet
            self.StockWallets.append(self.stockwallet)
            self.wallet += bet * bidvalue
            self.Wallets.append(self.wallet)
            self.profit = self.wallet + self.stockwallet * bidvalue
            self.Profits.append(self.profit)
            self.SellsT.append(time)
            self.SellsV.append(bidvalue)
        else:
            self.status = "Selling"
            self.currentbet = bet
        
    def Zero(self, bet, bidvalue, askvalue, time, targetvalue):
        if self.stockwallet > 0:
            if bidvalue >= targetvalue:
                self.ZeroT.append(time)
                self.ZeroV.append(bidvalue)
                self.ZeroType.append("Sell")
                self.wallet += bidvalue * bet
                self.Wallets.append(self.wallet)
                self.stockwallet -= bet
                self.StockWallets.append(self.stockwallet)
                self.profit = self.wallet + self.stockwallet * bidvalue
                self.Profits.append(self.profit)
            else:
                self.status = "ZSelling"
                self.currentbet = bet
        elif self.stockwallet < 0:
            if askvalue <= targetvalue:
                self.ZeroT.append(time)
                self.ZeroV.append(askvalue)
                self.ZeroType.append("Buy")
                self.wallet -= askvalue * bet
                self.Wallets.append(self.wallet)
                self.stockwallet += bet
                self.StockWallets.append(self.stockwallet)
                self.profit = self.wallet + self.stockwallet * askvalue
                self.Profits.append(self.profit)
            else:
                self.status = "ZBuying"
                self.currentbet = bet
        
    def Check(self, askvalue, bidvalue, time, targetvalue):
        self.waiting += 1
        if self.status == "ZSelling" or self.status == "Selling":
            if bidvalue >= targetvalue:
                if self.status == "ZSelling":
                    self.ZeroT.append(time)
                    self.ZeroV.append(bidvalue)
                    self.ZeroType.append("Sell")
                elif self.status == "Selling":
                    self.SellsT.append(time)
                    self.SellsV.append(bidvalue)
                self.wallet += self.currentbet * bidvalue
                self.Wallets.append(self.wallet)
                self.stockwallet -= self.currentbet
                self.StockWallets.append(self.stockwallet)
                self.profit = self.wallet + self.stockwallet * bidvalue
                self.Profits.append(self.profit)
                self.status = "clear"
                self.waiting = 0
        else:
            if askvalue <= targetvalue:
                if self.status == "ZBuying":
                    self.ZeroT.append(time)
                    self.ZeroV.append(askvalue)
                    self.ZeroType.append("Buy")
                elif self.status == "Buying":
                    self.BuysT.append(time)
                    self.BuysV.append(askvalue)
                self.wallet -= self.currentbet * askvalue
                self.Wallets.append(self.wallet)
                self.stockwallet += self.currentbet
                self.StockWallets.append(self.stockwallet)
                self.profit = self.wallet + self.stockwallet * askvalue
                self.Profits.append(self.profit)
                self.status = "clear"    
                self.waiting = 0
                
        if self.waiting >= 5:
            tolerance = 0.02
            if self.status == "ZSelling" or self.status == "Selling": 
                if bidvalue >= (targetvalue - tolerance):
                    if self.status == "ZSelling":
                        self.ZeroT.append(time)
                        self.ZeroV.append(bidvalue)
                        self.ZeroType.append("Sell")
                    elif self.status == "Selling":
                        self.SellsT.append(time)
                        self.SellsV.append(bidvalue)
                    self.wallet += self.currentbet * bidvalue
                    self.Wallets.append(self.wallet)
                    self.stockwallet -= self.currentbet
                    self.StockWallets.append(self.stockwallet)
                    self.profit = self.wallet + self.stockwallet * bidvalue
                    self.Profits.append(self.profit)
            else:
                if askvalue <= (targetvalue + tolerance):
                    if self.status == "ZBuying":
                        self.ZeroT.append(time)
                        self.ZeroV.append(askvalue)
                        self.ZeroType.append("Buy")
                    elif self.status == "Buying":
                        self.BuysT.append(time)
                        self.BuysV.append(askvalue)
                    self.wallet -= self.currentbet * askvalue
                    self.Wallets.append(self.wallet)
                    self.stockwallet += self.currentbet
                    self.StockWallets.append(self.stockwallet)
                    self.profit = self.wallet + self.stockwallet * askvalue
                    self.Profits.append(self.profit)
            self.status = "clear"  
            self.waiting = 0
        
    def Endseq(self):
        value = (self.BuysT[self.currentbuy:len(self.BuysT)], self.BuysV[self.currentbuy:len(self.BuysT)],
                 self.SellsT[self.currentsell:len(self.SellsT)], self.SellsV[self.currentsell:len(self.SellsV)],
                self.ZeroT[self.currentzero:len(self.ZeroT)], self.ZeroV[self.currentzero:len(self.ZeroV)], 
                self.Profits[self.currentzero:len(self.Profits)])

        self.currentbuy = len(self.BuysT)
        self.currentsell = len(self.SellsT)
        self.currentzero = len(self.ZeroT)
        
        return value

    def Endday(self, bet, bidvalue, askvalue, time):
        if self.stockwallet > 0:
            self.ZeroT.append(time)
            self.ZeroV.append(bidvalue)
            self.ZeroType.append("Sell")
            self.wallet += bidvalue * (self.stockwallet)
            self.Wallets.append(self.wallet)
            self.stockwallet = 0
            self.StockWallets.append(self.stockwallet)
            self.profit = self.wallet
            self.Profits.append(self.profit)
        elif self.stockwallet < 0:
            self.ZeroT.append(time)
            self.ZeroV.append(askvalue)
            self.ZeroType.append("Buy")
            self.wallet += askvalue * (self.stockwallet)
            self.Wallets.append(self.wallet)
            self.stockwallet = 0
            self.StockWallets.append(self.stockwallet)
            self.profit = self.wallet
            self.Profits.append(self.profit)
    
    def Reset(self):        
        self.currentbuy  = 0
        self.currentsell  = 0
        self.currentzero = 0
        
        self.profit = 0
        self.stockwallet = 0
        self.wallet = 0
        self.operate = 0
        self.oldsign = np.sign(0)
        self.lastvalue = 0
        
        self.ZeroT = []
        self.ZeroV = []
        self.ZeroType = []
        self.BuysT = []
        self.BuysV = []
        self.SellsT = []
        self.SellsV = []
        
        self.Profits =[]
        self.Wallets = []
        self.StockWallets = [] 