# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

class Ticks:
    def __init__ (self, h):
        self.AllDataFrames = []
        self.h = h
        self.currentday = 0
        self.currenttick = 0
        self.currentBid = 100
        self.currentAsk = 0

    def OpenData(self, daysrange, Data, DataPath):
        
        todel = []
        for i in range(len(daysrange)):
            if daysrange[i] in Data:
                df = pd.read_csv(f"{DataPath}{daysrange[i]}.csv", sep=";", decimal=".")
                df = df.dropna(axis=0)
                df["DATA"] = pd.to_datetime(df["DATA"], infer_datetime_format=True, dayfirst=True)
                self.AllDataFrames.append(df)
                print("Ok {0}".format(daysrange[i]))
            else:
                todel.append(i - len(daysrange))

        for i in todel:
            del(daysrange[i])

        
    def Filtra(self):
        
        #Retiar o leilão
        for i in range(len(self.AllDataFrames)):
            StartAuction = False
            for j in range(len(self.AllDataFrames[i])):
                if self.AllDataFrames[i]["ACAO"].iloc[j] == "TRADE":
                    StartAuction = True
                elif (StartAuction and (self.AllDataFrames[i]["ACAO"].iloc[j] == "BID" 
                                        or self.AllDataFrames[i]["ACAO"].iloc[j] == "ASK")):
                    inicut = j
                    break
            

            for j in range(1, len(self.AllDataFrames[i])):
                if self.AllDataFrames[i]["DATA"].iloc[-j].hour < 17:
                    endcut = len(self.AllDataFrames[i]) - j
                    break

            self.AllDataFrames[i] = self.AllDataFrames[i].drop(self.AllDataFrames[i].index[endcut : len(self.AllDataFrames[i])])
            self.AllDataFrames[i] = self.AllDataFrames[i].drop(self.AllDataFrames[i].index[0 : inicut])
            self.AllDataFrames[i] = self.AllDataFrames[i].reset_index(drop=True)
            
            
            counter = 0
            for j in range(10):
                if self.AllDataFrames[i]["ACAO"].iloc[j] == "TRADE":
                    counter+=1
            
            if counter >= 7:
                StartAuction = False
                for j in range(len(self.AllDataFrames[i])):
                    if self.AllDataFrames[i]["ACAO"].iloc[j+2] == "TRADE":
                        StartAuction = True
                    elif (StartAuction and (self.AllDataFrames[i]["ACAO"].iloc[j] == "BID" 
                                            or self.AllDataFrames[i]["ACAO"].iloc[j] == "ASK")):
                        inicut = j+2
                        break
                        
            self.AllDataFrames[i] = self.AllDataFrames[i].drop(self.AllDataFrames[i].index[0 : inicut])
        
        #Retira os volumens não inteiros
            self.AllDataFrames[i] = (self.AllDataFrames[i].loc[self.AllDataFrames[i]['VOLUME'] % 100 == 0]) 
            self.AllDataFrames[i] = (self.AllDataFrames[i].loc[self.AllDataFrames[i]['VALOR'] != 0])
            self.AllDataFrames[i] = self.AllDataFrames[i].reset_index(drop=True)

    def SendTick(self):
        currenttick = self.currenttick
        self.currenttick += self.h
        endtick = self.currenttick
        Times = []
        Value = []
        Volume =[]
        Asks = []
        Bids = []
        endday = False
        
        while currenttick <= endtick:
            if len(self.AllDataFrames[self.currentday]) > currenttick:
                if self.AllDataFrames[self.currentday]["ACAO"].iloc[currenttick]== "TRADE":
                    Times.append(self.AllDataFrames[self.currentday]["TIME"].iloc[currenttick])
                    Value.append(self.AllDataFrames[self.currentday]["VALOR"].iloc[currenttick])
                    Volume.append(self.AllDataFrames[self.currentday]["VOLUME"].iloc[currenttick])
                    Asks.append(self.currentAsk)
                    Bids.append(self.currentBid)
                elif self.AllDataFrames[self.currentday]["ACAO"].iloc[currenttick] == "BID":
                    self.currentBid = self.AllDataFrames[self.currentday]["VALOR"].iloc[currenttick]
                elif self.AllDataFrames[self.currentday]["ACAO"].iloc[currenttick] == "ASK":
                    self.currentAsk = self.AllDataFrames[self.currentday]["VALOR"].iloc[currenttick]
                currenttick += 1
            else:
                endday = True
                self.currentday += 1
                self.currenttick = 0
                break
        
        return Times, Value, Volume, Asks, Bids, endday
    
    def reseticks(self):
        self.currenttick = 0
        self.currentday = 0
