# -*- coding: utf-8 -*-
import numpy as np

class Signal_Derivates:
    def __init__(self, alpha, bet, Broker):
        self.alpha = alpha
        self.bet = bet
        self.Broker = Broker
        
        self.targetvalue = 0
        self.operate = 0
        self.oldsign = np.sign(0)
        self.lastvalue = 0

    def Recievetick(self, tick, ticks):

        for i in range(len(tick[0])):
            delta = tick[1][i] - self.lastvalue
            if delta != delta:
                delta = 0
                    
            askvalue = tick[2][i]
            bidvalue = tick[3][i]
            time = tick[0][i]
            
            if self.Broker.status == "clear":           
                self.targetvalue = tick[1][i]
    
                sign = np.sign(delta)
                #Neutro - Zera
                if sign != self.oldsign and self.operate != 0:
                    self.Broker.Zero(self.bet, bidvalue, askvalue, time, self.targetvalue)
                    self.operate = 0
                    
                #Vale - Compra
                if delta > self.alpha and self.operate == 0:
                    self.Broker.Buy(self.bet, askvalue, time, self.targetvalue)
                    self.operate = 1
    
                #Pico - Vende
                if delta < -self.alpha and self.operate == 0:
                    self.Broker.Sell(self.bet, bidvalue, time, self.targetvalue)
                    self.operate = -1
                    
            else:
                self.Broker.Check(askvalue, bidvalue, time, self.targetvalue)

            self.lastvalue = tick[1][i]
            self.oldsign = np.sign(delta)
            
            
        if tick[4]:
            #Faz a trade final do dia
            self.Broker.Endday(self.bet, bidvalue, askvalue, time)

        value = self.Broker.Endseq()
        
        return value
    
    def Reset(self):        
        self.operate = 0
        self.oldsign = np.sign(0)
        self.lastvalue = 0
        

class Signal_Derivates_Boosted:
    def __init__(self, alpha, bet, Broker):
        self.alpha = list(np.linspace(int(alpha/2), alpha*2, num=20, dtype=np.dtype(np.int16)))
        self.bet = bet
        
        self.Broker = Broker
        self.pool = 0
        
        self.targetvalue = 0
        self.operate = 0
        self.oldsign = np.sign(0)
        self.lastvalue = 0

    def Recievetick(self, tick, ticks):

        for i in range(len(tick[0])):
            self.pool = 0      
            
            delta = tick[1][i] - self.lastvalue
            if delta != delta:
                delta = 0
              
            for j in range(len(self.alpha)):
                if delta > self.alpha[j]: #Pool to buy
                    self.pool += 1
                if delta < -self.alpha[j]: #Pool to sell
                    self.pool -= 1
            
            sign = np.sign(delta)
            
            askvalue = tick[2][i]
            bidvalue = tick[3][i]
            time = tick[0][i]
            
            if self.Broker.status == "clear":           
                self.targetvalue = tick[1][i]
    
                sign = np.sign(delta)
                #Neutro - Zera
                if sign != self.oldsign and self.operate != 0:
                    self.Broker.Zero(self.bet, bidvalue, askvalue, time, self.targetvalue)
                    self.operate = 0
                    
                #Vale - Compra
                if self.pool > 0 and self.operate == 0:
                    self.Broker.Buy(self.bet, askvalue, time, self.targetvalue)
                    self.operate = 1
    
                #Pico - Vende
                if self.pool < 0 and self.operate == 0:
                    self.Broker.Sell(self.bet, bidvalue, time, self.targetvalue)
                    self.operate = -1
                    
            else:
                self.Broker.Check(askvalue, bidvalue, time, self.targetvalue)
            
            self.lastvalue = tick[1][i]
            self.oldsign = np.sign(delta)

        if tick[4]:
            #Faz a trade final do dia
            self.Broker.Endday(self.bet, bidvalue, askvalue, time)

        value = self.Broker.Endseq()
            
        return value
    
    def Reset(self):
        
        self.pool = 0
        self.operate = 0
        self.oldsign = np.sign(0)
        self.lastvalue = 0

        