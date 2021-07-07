# -*- coding: utf-8 -*-
import numpy as np

#Media Movel no tick
class MMt: 
    def __init__(self, freq):
        self.h = freq
        self.currenttick = 0
        self.currentday = 0
        self.Soma = []
        self.Data = []
        self.boost = False

    def Recievetick(self, tick, ticks): 
        self.currenttick += len(tick[1])
        if len(self.Soma) == 0:
            self.Data.append([])
            self.Data[self.currentday] = list(np.full(self.h, np.nan))
            
        for i in range(len(tick[1])):
            self.Soma.append(tick[1][i])
            if len(self.Soma) > self.h:
                del(self.Soma[0])
                self.Data[self.currentday].append(sum(self.Soma)/self.h)
                
        value = self.Data[self.currentday][self.currenttick-len(tick[1]): self.currenttick]
                
        if tick[2]:
            self.Soma = []
            self.currentday +=1
            self.currenttick = 0
            
        return value
    
    def Reset(self):
        self.Data = []
        self.Soma = []
        self.currentday = 0
        self.currenttick = 0

#Media Movel no Tempo
class MMT:
    def __init__(self, freq):
        self.h = freq
        self.currenttick = 0
        self.currentday = 0
        self.Soma = []
        self.Difs = []
        self.Data = []
        self.secMean = 0
        self.num = 0
        self.boost = False

    def Recievetick(self, tick, ticks): 
        self.currenttick += len(tick[1])
        oldtime = tick[0][0]
        if len(self.Soma) == 0:
            self.Data.append([])
            self.Soma = [0]
            self.Difs = [1]
        #Itera pelo dataframe para ver os passos
        for i in range(len(tick[0])):
            dif = tick[0][i] - oldtime
            
            if dif >= 1:
                if self.secMean != 0:
                    self.Soma[-1] = (self.Soma[-1]+self.secMean)/(self.num+1)
                    self.secMean = 0
                    self.num = 0
                for j in range(dif):
                    self.Difs.append(1)
                    self.Soma.append(tick[1][i])
                    
            if dif == 0:
                self.Difs.append(0)
                self.secMean += tick[1][i]
                self.num += 1
                
            if sum(self.Difs) >= self.h:
                resultado = sum(self.Soma)/len(self.Soma)
                self.Data[self.currentday].append(resultado)
                while sum(self.Difs) > self.h or self.Difs[0] != 1:
                    if self.Difs[0] == 1:
                        del(self.Soma[0])
                    del(self.Difs[0])
            else:
                self.Data[self.currentday].append(np.nan)
                
            oldtime = tick[0][i]

        value = self.Data[self.currentday][self.currenttick-len(tick[1]): self.currenttick]
                
        if tick[2]:
            self.Soma = []
            self.currentday +=1
            self.currenttick = 0
            
        return value
    
    def Reset(self):
        self.currenttick = 0
        self.currentday = 0
        self.Soma = []
        self.Difs = []
        self.Data = []
        self.secMean = 0
        self.num = 0

#Media Movel no Volume com passo adaptativo
class MMVA:
    def __init__(self, freq):
        self.h = freq
        self.hv = 0
        self.Hs = {}
        
        self.Difs = [1]
        self.Somavol = [0]
        
        self.cache = 0
        self.cachesum = 0
        self.counter = 1
        self.rest = 0
        
        self.Cacheprice = [0]
        self.Cachevol = [0]
        
        self.Volume = []
        self.Price = []
        self.Time = []
        
        self.AllVolume = []
        self.AllPrice = []
        self.AllTime = []
        
        self.oldtime = 0
        
        self.currentday = 0
        self.currentick = 0
        self.boost = False

        divvalue = 0
        for i in range(self.h+1):
            divvalue += i
        
        self.divvalue = divvalue

    def Recievetick(self, tick, ticks): 

        self.oldtime = tick[0][0]
        #Itera pelo dataframe para ver os passos
        for i in range(len(tick[0])):
            dif = tick[0][i] -self. oldtime
            if dif >= 1:
                for j in range(dif):
                    self.Difs.append(1)
                    self.Somavol.append(tick[3][i])
            if dif == 0:
                self.Difs.append(0)
                self.Somavol[-1] += tick[3][i]
            if sum(self.Difs) >= self.h:
                soma = 0
                for j in range(1, self.h+1):
                    soma += (self.h+1 - j) * self.Somavol[-j]
                resultado = soma/self.divvalue
                #resultado = np.mean(Somavol)
                self.Hs[tick[0][i]] = resultado
            if sum(self.Difs) > self.h:
                while sum(self.Difs) > self.h or self.Difs[0] != 1:
                    if self.Difs[0] == 1:
                        del(self.Somavol[0])
                    del(self.Difs[0])
            self.oldtime = tick[0][i]

        #Cria variaveis para discretizar o dataframe
        self.hv = 2500 * self.h
        self.oldtime = tick[0][0]

        #Itera pelo dataframe para ver os passos
        for i in range(len(tick[0])):
            self.cache = tick[3][i]
            self.Cachevol.append(self.cache)
            self.Cacheprice.append(tick[1][i])
            self.cachesum = sum(self.Cachevol)
            if self.cachesum >= self.hv:
                while self.cachesum >= self.hv:
                    #Cria Variaveis para a media ponderada
                    Valact = 0
                    Totact = 0
                    self.Volume.append(self.hv*self.counter)
                    self.Time.append(tick[0][i])
                    self.counter += 1
                    #Realiza media ponderada
                    for j in range(len(self.Cachevol)):
                        Valact += self.Cacheprice[j]*self.Cachevol[j]
                        Totact += self.Cachevol[j]
                    self.Price.append(Valact/Totact)
                    self.rest = (self.cachesum - self.hv)
                    if self.Cachevol[0] > self.rest:
                        self.Cachevol[0] -= self.rest + 1
                    else:
                        del(self.Cachevol[0])
                        del(self.Cacheprice[0])
                    self.cachesum = sum(self.Cachevol)
                #limpa o cache de volume mas mantem o resto como primeira entrada e atualiza o h
                if  self.oldtime - tick[0][i] >= self.h:
                    self.hv = self.h * self.Hs[tick[0][i]]
            else:
                self.Price.append(np.nan)
                self.Time.append(np.nan)
                self.Volume.append(np.nan)

            oldtime = tick[0][i]
            
        self.currentick += len(tick[0])
        
        value = (self.Price[self.currentick-len(tick[0]):self.currentick])
                
        if tick[2]:
            
            self.AllVolume.append(self.Volume)
            self.AllPrice.append(self.Price)
            self.AllTime.append(self.Time)
            
            self.hv = 0
            self.Hs = {}

            self.Difs = [1]
            self.Somavol = [0]

            self.cache = 0
            self.cachesum = 0
            self.counter = 1

            self.Cacheprice = [0]
            self.Cachevol = [0]

            self.Volume = []
            self.Price = []
            self.Time = []

            self.oldtime = 0
            
            self.currentday += 1
            self.currentick = 0
            
        return value
    
    def Reset(self):
        self.hv = 0
        self.Hs = {}
        
        self.Difs = [1]
        self.Somavol = [0]
        
        self.cache = 0
        self.cachesum = 0
        self.counter = 1
        
        self.Cacheprice = [0]
        self.Cachevol = [0]
        
        self.Volume = []
        self.Price = []
        self.Time = []
        
        self.AllVolume = []
        self.AllPrice = []
        self.AllTime = []
        
        self.oldtime = 0
        
        self.currentday = 0
        self.currentick = 0

#Media Movel no Volume
class MMV:
    def __init__(self, freq):
        self.h = freq
        self.hv = 1500*freq
        
        self.cache = 0
        self.cachesum = 0
        self.counter = 1
        self.rest = 0
        
        self.Cacheprice = [0]
        self.Cachevol = [0]
        
        self.Volume = []
        self.Price = []
        self.Time = []
        
        self.AllVolume = []
        self.AllPrice = []
        self.AllTime = []
        
        self.currentday = 0
        self.currentick = 0
        self.boost = False
        
        divvalue = 0
        for i in range(self.h+1):
            divvalue += i
        
        self.divvalue = divvalue

    def Recievetick(self, tick, ticks): 

        #Itera pelo dataframe para ver os passos
        for i in range(len(tick[0])):
            self.cache = tick[3][i]
            self.Cachevol.append(self.cache)
            self.Cacheprice.append(tick[1][i])
            self.cachesum = sum(self.Cachevol)
            if self.cachesum >= self.hv:
                while self.cachesum >= self.hv:
                    #Cria Variaveis para a media ponderada
                    Valact = 0
                    Totact = 0
                    self.Volume.append(self.hv*self.counter)
                    self.Time.append(tick[0][i])
                    self.counter += 1
                    #Realiza media ponderada
                    for j in range(len(self.Cachevol)):
                        Valact += self.Cacheprice[j]*self.Cachevol[j]
                        Totact += self.Cachevol[j]
                    self.Price.append(Valact/Totact)
                    self.rest = (self.cachesum - self.hv)
                    if self.Cachevol[0] > self.rest:
                        self.Cachevol[0] -= self.rest + 1
                    else:
                        del(self.Cachevol[0])
                        del(self.Cacheprice[0])
                    self.cachesum = sum(self.Cachevol)
                    
            else:
                self.Price.append(np.nan)
                self.Time.append(np.nan)
                self.Volume.append(np.nan)
           
        self.currentick += len(tick[0])
        
        value = (self.Price[self.currentick-len(tick[0]):self.currentick])
                
        if tick[2]:
            
            self.AllVolume.append(self.Volume)
            self.AllPrice.append(self.Price)
            self.AllTime.append(self.Time)
            
            self.cache = 0
            self.cachesum = 0
            self.counter = 1

            self.Cacheprice = [0]
            self.Cachevol = [0]

            self.Volume = []
            self.Price = []
            self.Time = []

            self.oldtime = 0
            
            self.currentday += 1
            self.currentick = 0
            
        return value
    
    def Reset(self):          
        self.cache = 0
        self.cachesum = 0
        self.counter = 1
        
        self.Cacheprice = [0]
        self.Cachevol = [0]
        
        self.Volume = []
        self.Price = []
        self.Time = []
        
        self.AllVolume = []
        self.AllPrice = []
        self.AllTime = []
        
        self.currentday = 0
        self.currentick = 0
        
#Media Movel no Volume com boost
class MMt_Boost: 
    def __init__(self, freq):
        self.h = list(np.linspace(int(freq/2), freq*2, num=20, dtype=np.dtype(np.int16)))
        self.currenttick = 0
        self.currentday = 0
        self.currentdaybegin = True
        self.currenth = 0
        self.Soma = []
        self.ValueData = []
        self.TimeData = []
        self.boost = False
        
    def Recievetick(self, tick, ticks): 
        if self.currentdaybegin:
            self.currentdaybegin = False
            self.ValueData.append([])
            self.TimeData.append([])
            for i in range(len(self.h)):
                self.Soma.append([])
                self.ValueData[self.currentday].append([])
                self.TimeData[self.currentday].append([])
                self.ValueData[self.currentday][i] = list(np.full(self.h[i], np.nan))
                self.TimeData[self.currentday][i] = list(np.full(self.h[i], np.nan))
    
        self.currenth = 0
        self.currenttick += len(tick[1])
        for i in range(len(self.h)):
            for j in range(len(tick[1])):
                self.Soma[i].append(tick[1][j])
                if len(self.Soma[i]) > self.h[i]:
                    del(self.Soma[i][0])
                    self.ValueData[self.currentday][self.currenth].append(sum(self.Soma[i])/self.h[i])
                    self.TimeData[self.currentday][self.currenth].append(tick[0][j])    
                    
            self.currenth += 1
            
        value = []
        time = []
        for i in range(len(self.ValueData[self.currentday])):
            value.append(self.ValueData[self.currentday][i][self.currenttick-len(tick[1]): self.currenttick])
            time.append(self.TimeData[self.currentday][i][self.currenttick-len(tick[1]): self.currenttick])
              
        if tick[2]:
            self.Soma = []
            self.currentday +=1
            self.currenttick = 0
            self.currentdaybegin = True
            
        return time, value
    
    def Reset(self):
        self.ValueData = []
        self.TimeData = []
        self.Soma = []
        self.currentday = 0
        self.currenttick = 0