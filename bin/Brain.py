# -*- coding: utf-8 -*-
import time
from .Register import Register
from .Optimize import Optimizer

class Runner:
    def __init__(self):
        self.active = True
        
        self.opt = 0
        self.Reg = Register()
        
    def Runstd(self, Menu, daysrange):
        Menu.Source.reseticks()
        Menu.Model.Reset()
        DoTrades = (Menu.variables[6].get() != "No Trades")
        if DoTrades:
            Menu.Signal.Reset()
            Menu.Broker.Reset()
        day = 0
    
        for i in range(len(daysrange)):
            if Menu.kill:
                break
            x = []
            y = []
            xm =[]
            ym =[]
            asks = []
            bids = []
            buysT = []
            buysV = []
            sellsT = []
            sellsV = []
            zerosT =[]
            zerosV =[]
            profits = []
            daychange = False

            while not daychange:
                if Menu.kill:
                    break
                #Envia Ticks
                morex, morey, morevolume, moreasks, morebids, daychange = Menu.Source.SendTick()
                x += morex
                y += morey
                asks += moreasks
                bids += morebids
                #Chama o Modelo
                moreym = Menu.Model.Recievetick((morex, morey, daychange, morevolume), Menu.Source)
                xm += morex
                ym += moreym
                #Limpa os gráficos                 
                Menu.subplot[0].clear()
                Menu.subplot[1].clear()
                Menu.subplot[2].clear()
                #Se estiver fazendo trades usa o broker
                if DoTrades:
                    morebuysT, morebuysV, moresellsT, moresellsV, morezeroT, morezeroV, moreprofit = Menu.Signal.Recievetick(
                                        (morex, moreym, moreasks, morebids, daychange), Menu.Source)
                    buysT += morebuysT
                    buysV += morebuysV
                    sellsT += moresellsT
                    sellsV += moresellsV
                    zerosT += morezeroT
                    zerosV += morezeroV
                    profits += moreprofit
                
                #Plota o primeiro gráfico
                Menu.subplot[0].plot(x, y, "k")
                Menu.subplot[0].plot(xm, ym, "b")
                #Altera os valores do ask e Bid                
                Menu.Ask[1].config(text=asks[-1])
                Menu.Bid[1].config(text=bids[-1])
                
                #Plota os gráficos de Trade e lucro
                if DoTrades:
                    #Plota os gráficos de Trade
                    Menu.subplot[1].plot(buysT, buysV, "go")
                    Menu.subplot[1].plot(sellsT, sellsV, "ro")
                    Menu.subplot[1].plot(zerosT, zerosV, "o", color="darkgrey")
                    #Plota o gráfico de lucro
                    OperationsT = (buysT + sellsT + zerosT)
                    OperationsT = sorted(OperationsT)
                    if len(Menu.Broker.Profits) > 0:
                        Menu.subplot[2].plot(OperationsT, Menu.Broker.Profits)
                    #Altera os valores dos numeros de trades e do lucro final
                    Trades = len(OperationsT)
                    Menu.Trades[1].config(text=Trades)
                    TradesT = self.Reg.TradesT + Trades
                    Menu.TradesT[1].config(text= TradesT)
                    
                    if len(Menu.Broker.Profits) > 0:
                        Total = round(Menu.Broker.Profits[-1] - Trades*21*Menu.Signal.bet*(0.024/100),2)
                        Menu.Total[1].config(text=Total)
                        TotalG = round(self.Reg.TotalG + Total, 2)
                        Menu.TotalG[1].config(text=TotalG)
                    
                    
                #Altera o eixo do gráfico para corresponder ao dia
                Menu.subplot[0].axes.set_xlim([Menu.Source.AllDataFrames[i]["TIME"].iloc[0], 
                                        Menu.Source.AllDataFrames[i]["TIME"].iloc[-1]])
                Menu.subplot[1].axes.set_xlim([Menu.Source.AllDataFrames[i]["TIME"].iloc[0], 
                                        Menu.Source.AllDataFrames[i]["TIME"].iloc[-1]])
                Menu.subplot[2].axes.set_xlim([Menu.Source.AllDataFrames[i]["TIME"].iloc[0], 
                                        Menu.Source.AllDataFrames[i]["TIME"].iloc[-1]])
                #Atualiza os widgets
                Menu.NameGraph()
                Menu.canvas.draw()
                                
                Menu.window.update()

                time.sleep(0.5)
                
                if daychange:
                    day += 1
                    self.Reg.Register(Menu.Broker.ZeroT, Menu.Broker.ZeroV, Menu.Broker.ZeroType, Menu.Broker.BuysT,
                                      Menu.Broker.SellsT, Menu.Broker.BuysV, Menu.Broker.SellsV, Menu.Broker.Profits, 
                                      Menu.Broker.Wallets, Menu.Broker.StockWallets, Trades, Total)
                    
                    if day == len(Menu.Source.AllDataFrames):
                        self.Reg.Export()
                        Menu.Debugprogramend()
                    
                    else:
                        Menu.Debugdayend()
                        if DoTrades:
                            Menu.Broker.Reset()
                            Menu.Signal.Reset()
                        time.sleep(5)

                        
    #Run para modelo Boosted e Bot Normal
    def RunModelB(self, Menu, daysrange):
        self.opt = Optimizer()
        Menu.Source.reseticks()
        Menu.Model.Reset()
        DoTrades = (Menu.variables[6].get() != "No Trades")
        if DoTrades:
            Menu.Signal.Reset()
            Menu.Broker.Reset()
        day = 0
                    
        for i in range(len(daysrange)):
            if Menu.kill:
                break
            x = []
            y = []
            xm =[]
            ym =[]
            xmopt = []
            ymopt = []
            asks = []
            bids = []
            buysT = []
            buysV = []
            sellsT = []
            sellsV = []
            zerosT =[]
            zerosV =[]
            profits = []
            daychange = False

            while not daychange:
                if Menu.kill:
                    break
                #Envia Ticks
                morex, morey, morevolume, moreasks, morebids, daychange = Menu.Source.SendTick()
                x += morex
                y += morey
                asks += moreasks
                bids += morebids
                #Chama o Modelo
                morexm, moreym = Menu.Model.Recievetick((morex, morey, daychange, morevolume), Menu.Source)
                if len(xm) == 0:
                    for j in range(len(moreym)):
                        xm.append([])
                        ym.append([])
                for j in range(len(moreym)):
                    xm[j] += morexm[j]
                    ym[j] += moreym[j]
                    
                morexmopt, moreymopt = self.opt.Med1D(morexm, moreym)
                xmopt += morexmopt
                ymopt += moreymopt
                #Limpa os gráficos
                Menu.subplot[0].clear()
                Menu.subplot[1].clear()
                Menu.subplot[2].clear()
                #Se estiver fazendo trades usa o broker
                if DoTrades:
                    morebuysT, morebuysV, moresellsT, moresellsV, morezeroT, morezeroV, moreprofit = Menu.Signal.Recievetick(
                                        (morex, moreymopt, moreasks, morebids, daychange), Menu.Source)
                    buysT += morebuysT
                    buysV += morebuysV
                    sellsT += moresellsT
                    sellsV += moresellsV
                    zerosT += morezeroT
                    zerosV += morezeroV
                    profits += moreprofit
                                    
                #Plota o primeiro gráfico

#               #Usar paraplotar todas os hs
#                for j in range(len(moreym)):
#                    Menu.subplot[0].plot(xm[j], ym[j], "b")
                #Usar para plotar apenas o otimizada
                Menu.subplot[0].plot(x, y, "k")
                Menu.subplot[0].plot(xmopt, ymopt, "b")

                #Altera os valores do ask e Bid
                if len(asks) == 0 or len(bids) == 0:
                    Menu.Ask[1].config(text="---")
                    Menu.Bid[1].config(text="---")
                else:
                    Menu.Ask[1].config(text=asks[-1])
                    Menu.Bid[1].config(text=bids[-1])
                
                #Plota os gráficos de Trade e lucro
                if DoTrades:
                    #Plota os gráficos de Trade
                    Menu.subplot[1].plot(buysT, buysV, "go")
                    Menu.subplot[1].plot(sellsT, sellsV, "ro")
                    Menu.subplot[1].plot(zerosT, zerosV, "o", color="darkgrey")
                    #Plota o gráfico de lucro
                    OperationsT = (buysT + sellsT + zerosT)
                    OperationsT = sorted(OperationsT)
                    if len(Menu.Broker.Profits) > 0:
                        Menu.subplot[2].plot(OperationsT, Menu.Broker.Profits)
                    #Altera os valores dos numeros de trades e do lucro final
                    Trades = len(OperationsT)
                    Menu.Trades[1].config(text=Trades)
                    TradesT = self.Reg.TradesT + Trades
                    Menu.TradesT[1].config(text= TradesT)
                    
                    if len(Menu.Broker.Profits) > 0:
                        Total = round(Menu.Broker.Profits[-1] - Trades*21*Menu.Signal.bet*(0.024/100),2)
                        Menu.Total[1].config(text=Total)
                        TotalG = round(self.Reg.TotalG + Total, 2)
                        Menu.TotalG[1].config(text=TotalG)
                    
                #Altera o eixo do gráfico para corresponder ao dia
                Menu.subplot[0].axes.set_xlim([Menu.Source.AllDataFrames[i]["TIME"].iloc[0], 
                                        Menu.Source.AllDataFrames[i]["TIME"].iloc[-1]])
                Menu.subplot[1].axes.set_xlim([Menu.Source.AllDataFrames[i]["TIME"].iloc[0], 
                                        Menu.Source.AllDataFrames[i]["TIME"].iloc[-1]])
                Menu.subplot[2].axes.set_xlim([Menu.Source.AllDataFrames[i]["TIME"].iloc[0], 
                                        Menu.Source.AllDataFrames[i]["TIME"].iloc[-1]])
                #Atualiza os widgets
                Menu.NameGraph()
                Menu.canvas.draw()
                                
                Menu.window.update()

                time.sleep(0.5)
                
                if daychange:
                    day += 1
                    self.Reg.Register(Menu.Broker.ZeroT, Menu.Broker.ZeroV, Menu.Broker.ZeroType, Menu.Broker.BuysT,
                                      Menu.Broker.SellsT, Menu.Broker.BuysV, Menu.Broker.SellsV, Menu.Broker.Profits, 
                                      Menu.Broker.Wallets, Menu.Broker.StockWallets, Trades, Total)
                    
                    if day == len(Menu.Source.AllDataFrames):
                        self.Reg.Export()
                        Menu.Debugprogramend()
                    
                    else:
                        Menu.Debugdayend()
                        if DoTrades:
                            Menu.Broker.Reset()
                            Menu.Signal.Reset()
                        time.sleep(5)
    
    #Run para Signal Boosted e modelo normal
    def RunBotB(self, Menu, daysrange):
        Menu.Source.reseticks()
        Menu.Model.Reset()
        DoTrades = (Menu.variables[6].get() != "No Trades")
        if DoTrades:
            Menu.Signal.Reset()
            Menu.Broker.Reset()
        day = 0
    
        for i in range(len(daysrange)):
            if Menu.kill:
                break
            x = []
            y = []
            xm =[]
            ym =[]
            asks = []
            bids = []
            buysT = []
            buysV = []
            sellsT = []
            sellsV = []
            zerosT =[]
            zerosV =[]
            profits = []
            daychange = False

            while not daychange:
                if Menu.kill:
                    break
                #Envia Ticks
                morex, morey, morevolume, moreasks, morebids, daychange = Menu.Source.SendTick()
                x += morex
                y += morey
                asks += moreasks
                bids += morebids
                #Chama o Modelo
                moreym = Menu.Model.Recievetick((morex, morey, daychange, morevolume), Menu.Source)
                xm += morex
                ym += moreym
                #Limpa os gráficos                 
                Menu.subplot[0].clear()
                Menu.subplot[1].clear()
                Menu.subplot[2].clear()
                #Se estiver fazendo trades usa o broker
                if DoTrades:
                    morebuysT, morebuysV, moresellsT, moresellsV, morezeroT, morezeroV, moreprofit = Menu.Signal.Recievetick(
                                        (morex, moreym, moreasks, morebids, daychange), Menu.Source)
                    buysT += morebuysT
                    buysV += morebuysV
                    sellsT += moresellsT
                    sellsV += moresellsV
                    zerosT += morezeroT
                    zerosV += morezeroV
                    profits += moreprofit
                
                #Plota o primeiro gráfico
                Menu.subplot[0].plot(x, y, "k")
                Menu.subplot[0].plot(xm, ym, "b")
                #Altera os valores do ask e Bid                
                Menu.Ask[1].config(text=asks[-1])
                Menu.Bid[1].config(text=bids[-1])
                
                #Plota os gráficos de Trade e lucro
                if DoTrades:
                    #Plota os gráficos de Trade
                    Menu.subplot[1].plot(buysT, buysV, "go")
                    Menu.subplot[1].plot(sellsT, sellsV, "ro")
                    Menu.subplot[1].plot(zerosT, zerosV, "o", color="darkgrey")
                    #Plota o gráfico de lucro
                    OperationsT = (buysT + sellsT + zerosT)
                    OperationsT = sorted(OperationsT)
                    if len(Menu.Broker.Profits) > 0:
                        Menu.subplot[2].plot(OperationsT, Menu.Broker.Profits)
                    #Altera os valores dos numeros de trades e do lucro final
                    Trades = len(OperationsT)
                    Menu.Trades[1].config(text=Trades)
                    TradesT = self.Reg.TradesT + Trades
                    Menu.TradesT[1].config(text= TradesT)
                    
                    if len(Menu.Broker.Profits) > 0:
                        Total = round(Menu.Broker.Profits[-1] - Trades*21*Menu.Signal.bet*(0.024/100),2)
                        Menu.Total[1].config(text=Total)
                        TotalG = round(self.Reg.TotalG + Total, 2)
                        Menu.TotalG[1].config(text=TotalG)
                    
                #Altera o eixo do gráfico para corresponder ao dia
                Menu.subplot[0].axes.set_xlim([Menu.Source.AllDataFrames[i]["TIME"].iloc[0], 
                                        Menu.Source.AllDataFrames[i]["TIME"].iloc[-1]])
                Menu.subplot[1].axes.set_xlim([Menu.Source.AllDataFrames[i]["TIME"].iloc[0], 
                                        Menu.Source.AllDataFrames[i]["TIME"].iloc[-1]])
                Menu.subplot[2].axes.set_xlim([Menu.Source.AllDataFrames[i]["TIME"].iloc[0], 
                                        Menu.Source.AllDataFrames[i]["TIME"].iloc[-1]])
                #Atualiza os widgets
                Menu.NameGraph()
                Menu.canvas.draw()
                                
                Menu.window.update()

                time.sleep(0.5)
                
                if daychange:
                    day += 1
                    self.Reg.Register(Menu.Broker.ZeroT, Menu.Broker.ZeroV, Menu.Broker.ZeroType, Menu.Broker.BuysT,
                                      Menu.Broker.SellsT, Menu.Broker.BuysV, Menu.Broker.SellsV, Menu.Broker.Profits, 
                                      Menu.Broker.Wallets, Menu.Broker.StockWallets, Trades, Total)
                    
                    if day == len(Menu.Source.AllDataFrames):
                        self.Reg.Export()
                        Menu.Debugprogramend()
                    
                    else:
                        Menu.Debugdayend()
                        if DoTrades:
                            Menu.Broker.Reset()
                            Menu.Signal.Reset()
                        time.sleep(5)
    
    #Run para modelo e Sinal Boosted
    def RunAllB(self, Menu, daysrange):
        self.opt = Optimizer()
        Menu.Source.reseticks()
        Menu.Model.Reset()
        DoTrades = (Menu.variables[6].get() != "No Trades")
        if DoTrades:
            Menu.Signal.Reset()
            Menu.Broker.Reset()
        day = 0
    
        for i in range(len(daysrange)):
            if Menu.kill:
                break
            x = []
            y = []
            xm =[]
            ym =[]
            xmopt = []
            ymopt = []
            asks = []
            bids = []
            buysT = []
            buysV = []
            sellsT = []
            sellsV = []
            zerosT =[]
            zerosV =[]
            profits = []
            daychange = False

            while not daychange:
                if Menu.kill:
                    break
                #Envia Ticks
                morex, morey, morevolume, moreasks, morebids, daychange = Menu.Source.SendTick()
                x += morex
                y += morey
                asks += moreasks
                bids += morebids
                #Chama o Modelo
                morexm, moreym = Menu.Model.Recievetick((morex, morey, daychange, morevolume), Menu.Source)
                if len(xm) == 0:
                    for j in range(len(moreym)):
                        xm.append([])
                        ym.append([])
                for j in range(len(moreym)):
                    xm[j] += morexm[j]
                    ym[j] += moreym[j]
                    
                morexmopt, moreymopt = self.opt.Med1D(morexm, moreym)
                xmopt += morexmopt
                ymopt += moreymopt
                #Limpa os gráficos
                Menu.subplot[0].clear()
                Menu.subplot[1].clear()
                Menu.subplot[2].clear()
                #Se estiver fazendo trades usa o broker
                if DoTrades:
                    morebuysT, morebuysV, moresellsT, moresellsV, morezeroT, morezeroV, moreprofit = Menu.Signal.Recievetick(
                                        (morex, moreymopt, moreasks, morebids, daychange), Menu.Source)
                    buysT += morebuysT
                    buysV += morebuysV
                    sellsT += moresellsT
                    sellsV += moresellsV
                    zerosT += morezeroT
                    zerosV += morezeroV
                    profits += moreprofit
                                    
                #Plota o primeiro gráfico
                
#               #Usar paraplotar todas os hs
#                for j in range(len(moreym)):
#                    Menu.subplot[0].plot(xm[j], ym[j], "b")
                #Usar para plotar apenas o otimizada
                Menu.subplot[0].plot(x, y, "k")
                Menu.subplot[0].plot(xmopt, ymopt, "b")
                
                #Altera os valores do ask e Bid                
                Menu.Ask[1].config(text=asks[-1])
                Menu.Bid[1].config(text=bids[-1])
                
                #Plota os gráficos de Trade e lucro
                if DoTrades:
                    #Plota os gráficos de Trade
                    Menu.subplot[1].plot(buysT, buysV, "go")
                    Menu.subplot[1].plot(sellsT, sellsV, "ro")
                    Menu.subplot[1].plot(zerosT, zerosV, "o", color="darkgrey")
                    #Plota o gráfico de lucro
                    OperationsT = (buysT + sellsT + zerosT)
                    OperationsT = sorted(OperationsT)
                    if len(Menu.Broker.Profits) > 0:
                        Menu.subplot[2].plot(OperationsT, Menu.Broker.Profits)
                    #Altera os valores dos numeros de trades e do lucro final
                    Trades = len(OperationsT)
                    Menu.Trades[1].config(text=Trades)
                    TradesT = self.Reg.TradesT + Trades
                    Menu.TradesT[1].config(text= TradesT)
                    
                    if len(Menu.Broker.Profits) > 0:
                        Total = round(Menu.Broker.Profits[-1] - Trades*21*Menu.Signal.bet*(0.024/100),2)
                        Menu.Total[1].config(text=Total)
                        TotalG = round(self.Reg.TotalG + Total, 2)
                        Menu.TotalG[1].config(text=TotalG)
                    
                #Altera o eixo do gráfico para corresponder ao dia
                Menu.subplot[0].axes.set_xlim([Menu.Source.AllDataFrames[i]["TIME"].iloc[0], 
                                        Menu.Source.AllDataFrames[i]["TIME"].iloc[-1]])
                Menu.subplot[1].axes.set_xlim([Menu.Source.AllDataFrames[i]["TIME"].iloc[0], 
                                        Menu.Source.AllDataFrames[i]["TIME"].iloc[-1]])
                Menu.subplot[2].axes.set_xlim([Menu.Source.AllDataFrames[i]["TIME"].iloc[0], 
                                        Menu.Source.AllDataFrames[i]["TIME"].iloc[-1]])
                #Atualiza os widgets
                Menu.NameGraph()
                Menu.canvas.draw()
                                
                Menu.window.update()

                time.sleep(0.5)
                
                if daychange:
                    day += 1
                    self.Reg.Register(Menu.Broker.ZeroT, Menu.Broker.ZeroV, Menu.Broker.ZeroType, Menu.Broker.BuysT,
                                      Menu.Broker.SellsT, Menu.Broker.BuysV, Menu.Broker.SellsV, Menu.Broker.Profits, 
                                      Menu.Broker.Wallets, Menu.Broker.StockWallets, Trades, Total)
                    
                    if day == len(Menu.Source.AllDataFrames):
                        self.Reg.Export()
                        Menu.Debugprogramend()
                    
                    else:
                        Menu.Debugdayend()
                        if DoTrades:
                            Menu.Broker.Reset()
                            Menu.Signal.Reset()
                        time.sleep(5)