# -*- coding: utf-8 -*-
from tkinter import *
from .Source_UNIX import Ticks
from .Brain import Runner

class Menu():
    def __init__(self, Data, DataPath):

        #Lista para os elementos da tela
        self.widgets = []
        self.startbuttom = 0
        self.kill = False
        #Lista os elementos ativos da tela
        self.active = []
        #Lista de posições
        self.positions = []
        #lista das variaveis
        self.variables = []
        #Guarda o gráfico
        self.fig = 0
        self.subplot = []
        #lista dos dados disponiveis
        self.Data = Data
        self.DataPath = DataPath
        #Canvas do plot
        self.window = 0
        self.Canvas = 0
        #Fonte, Modelo, Sinal e Broker
        self.Broker = 0
        self.Signal = 0
        self.Model = 0
        self.Source = 0
        #Boosts em uso
        self.ModelBoost = False
        self.SignalBoost = False
        #Bid, Ask e Total
        self.Bid = []
        self.Ask = []
        self.Trades = []
        self.TradesT = []
        self.Total = []
        self.TotalG = []

    def toggle_entry(self, widget):
        if self.active[widget]:
            self.widgets[widget].place_forget()
            self.active[widget] = False
        else:
            self.widgets[widget].place(x=self.positions[widget][0], y=self.positions[widget][1])
            self.active[widget] = True
            
    def activate_entry(self, widget):
        if not self.active[widget]:
            self.widgets[widget].place(x=self.positions[widget][0], y=self.positions[widget][1])
            self.active[widget] = True
            
    def deactivate_entry(self, widget):
        if self.active[widget]:
            self.widgets[widget].place_forget()
            self.active[widget] = False 
            
    def Showmoredays(self, *args):
        self.toggle_entry(4)
        self.toggle_entry(5)
    
    def Showbot(self, *args):
        kind = self.variables[6].get()
        if kind == "No Trades":
            self.deactivate_entry(14)
            self.deactivate_entry(15)
            self.deactivate_entry(16)
            self.deactivate_entry(17)
            self.deactivate_entry(18)
            self.deactivate_entry(19)
        elif kind == "Derivates (Alpha)":
            self.activate_entry(14)
            self.activate_entry(15)
            self.activate_entry(16)
            self.activate_entry(17)
            self.activate_entry(18)
            self.activate_entry(19)
        elif kind == "Derivates Boosted":
            self.activate_entry(14)
            self.activate_entry(15)
            self.activate_entry(16)
            self.activate_entry(17)
            self.activate_entry(18)
            self.activate_entry(19)
    
    def Build_Variables(self, window):
        
        self.window = window
        
        dayini = StringVar(window)
        dayini.set("Select...")
        
        moredays = IntVar(window)
        moredays.set(1)
        moredays.trace("w", self.Showmoredays)
        
        dayend = StringVar(window)
        dayend.set("Select...")
        
        plotspeed = IntVar(window)
        plotspeed.set(500)
        
        model = StringVar(window)
        model.set("Ticks Rolling Mean")
        
        modelh = IntVar(window)
        modelh.set(250)
        
        signalkind = StringVar(window)
        signalkind.set("Derivates (Alpha)")
        signalkind.trace("w", self.Showbot)
        
        signalalpha = DoubleVar(window)
        signalalpha.set(5e-5)
        
        brokerkind = StringVar(window)
        brokerkind.set("Standard")
        brokerkind.trace("w", self.Showbot)
        
        brokerbet = IntVar(window)
        brokerbet.set(100)
        
        self.variables.append(dayini)     #0
        self.variables.append(moredays)   #1
        self.variables.append(dayend)     #2
        self.variables.append(plotspeed)  #3
        self.variables.append(model)      #4
        self.variables.append(modelh)     #5
        self.variables.append(signalkind) #6
        self.variables.append(signalalpha)#7
        self.variables.append(brokerkind) #8
        self.variables.append(brokerbet)  #9
    
    def Build_Fields(self, window):       #Constroi o Menu
        
        widheight = 200
        heightdif = 50
        labelx = 100
        varx = 300
        
        Titulo = Label(window)
        Titulo.config(text="Tick-by-tick Simulator", bg = "white")
        Titulo.config(height = 2 , width = 20)
        Titulo.place(x=labelx, y= 50)

        Data = self.Data
    #--- Initial Day
        DayiniLabel = Label(window)
        DayiniLabel.config(text="Starting Day:", font=("arial", 12), bg = "grey")
        DayiniLabel.config(height = 2 , width = 20)
        DayiniLabel.place(x=labelx, y=widheight)
        
        Dayini = OptionMenu(window, self.variables[0], *Data)
        Dayini.place(x=varx, y=widheight)
        widheight+=heightdif
    #--- Days Checkbox
        MoredaysLabel = Label(window)
        MoredaysLabel.config(text="Multiple Days:", font=("arial", 12), bg = "grey")
        MoredaysLabel.config(height = 2 , width = 20)
        MoredaysLabel.place(x=labelx, y= widheight)
        
        Moredays = Checkbutton(window, variable=self.variables[1])
        Moredays.place(x=varx, y= widheight)
        widheight+=heightdif
    #--- End Day
        DayendLabel = Label(window)
        DayendLabel.config(text="Ending Day:", font=("arial", 12), bg = "grey")
        DayendLabel.config(height = 2 , width = 20)
        DayendLabel.place(x=labelx, y= widheight)
        
        Dayend = OptionMenu(window, self.variables[2], *Data)
        Dayend.place(x=varx, y= widheight)
        widheight+=heightdif
    #--- #Plot Speed
        PlotspeedLabel = Label(window)
        PlotspeedLabel.config(text="Update Frequency:", font=("arial", 12), bg = "grey")
        PlotspeedLabel.config(height = 2 , width = 20)
        PlotspeedLabel.place(x=labelx, y= widheight)
        
        Plotspeed = Scale(window, from_=1, to=10000, resolution=10, 
                          orient=HORIZONTAL, variable=self.variables[3])
        Plotspeed.place(x=varx, y= widheight)
        widheight+=heightdif
    #--- Model      
        ModelLabel = Label(window)
        ModelLabel.config(text="Model:", font=("arial", 12), bg = "grey")
        ModelLabel.config(height = 2 , width = 20)
        ModelLabel.place(x=labelx, y= widheight)
        
        modelops = ["Ticks Rolling Mean", "Time Rolling Mean", "Volume Rolling Mean", 
                    "Volume Adapt Rolling Mean", "Ticks Boost Rolling Mean"]
        Model = OptionMenu(window, self.variables[4], *modelops)
        Model.place(x=varx, y= widheight)
        widheight+=heightdif
    #--- Model h
        ModelhLabel = Label(window)
        ModelhLabel.config(text="Model Step:", font=("arial", 12), bg = "grey")
        ModelhLabel.config(height = 2 , width = 20)
        ModelhLabel.place(x=labelx, y= widheight)
        
        Modelh = Scale(window, from_=0, to=2000, resolution=1, 
                       orient=HORIZONTAL, variable=self.variables[5])
        Modelh.place(x=varx, y= widheight)
        widheight+=heightdif
    #-- Signal type
        SignalkindLabel = Label(window)
        SignalkindLabel.config(text="Signal:", font=("arial", 12), bg = "grey")
        SignalkindLabel.config(height = 2 , width = 20)
        SignalkindLabel.place(x=labelx, y= widheight)
        
        Signalops = ["No Trades", "Derivates (Alpha)", "Derivates Boosted"]
        Signalkind = OptionMenu(window, self.variables[6], *Signalops)
        Signalkind.place(x=varx, y= widheight)
        widheight+=heightdif
    #-- Signal Alpha
        SignalalphaLabel = Label(window)
        SignalalphaLabel.config(text="Signal Alpha:", font=("arial", 12), bg = "grey")
        SignalalphaLabel.config(height = 2 , width = 20)
        SignalalphaLabel.place(x=labelx, y= widheight)
        
        Botalpha = Scale(window, from_=0.00001, to=0.0005, resolution=0.00001, 
                         orient=HORIZONTAL, variable=self.variables[7])
        Botalpha.place(x=varx, y= widheight)
        widheight+=heightdif
    #-- Broker type
        BrokerkindLabel = Label(window)
        BrokerkindLabel.config(text="Broker:", font=("arial", 12), bg = "grey")
        BrokerkindLabel.config(height = 2 , width = 20)
        BrokerkindLabel.place(x=labelx, y= widheight)
        
        Brokerops = ["Standard", "Waiter"]
        Brokerkind = OptionMenu(window, self.variables[8], *Brokerops)
        Brokerkind.place(x=varx, y= widheight)
        widheight+=heightdif
    
    #-- Broker Bet
        BrokerbetLabel = Label(window)
        BrokerbetLabel.config(text="Stocks Bought:", font=("arial", 12), bg = "grey")
        BrokerbetLabel.config(height = 2 , width = 20)
        BrokerbetLabel.place(x=labelx, y= widheight)
        
        Brokerbet = Scale(window, from_=0, to=1000, resolution=100, 
                       orient=HORIZONTAL, variable=self.variables[9])
        Brokerbet.place(x=varx, y= widheight)
        widheight+=heightdif

    #--- adiciona  itens criados a lista
        self.widgets.append(DayiniLabel)            #0
        self.widgets.append(Dayini)                 #1
        self.widgets.append(MoredaysLabel)          #2
        self.widgets.append(Moredays)               #3
        self.widgets.append(DayendLabel)            #4
        self.widgets.append(Dayend)                 #5
        self.widgets.append(PlotspeedLabel)         #6
        self.widgets.append(Plotspeed)              #7
        self.widgets.append(ModelLabel)             #8
        self.widgets.append(Model)                  #9
        self.widgets.append(ModelhLabel)            #10
        self.widgets.append(Modelh)                 #11
        self.widgets.append(SignalkindLabel)        #12
        self.widgets.append(Signalkind)             #13
        self.widgets.append(SignalalphaLabel)       #14
        self.widgets.append(Botalpha)               #15
        self.widgets.append(BrokerkindLabel)        #16
        self.widgets.append(Brokerkind)             #17
        self.widgets.append(BrokerbetLabel)         #18
        self.widgets.append(Brokerbet)              #19
    #adiciona oswidgets a lista de ativados
        for i in range(len(self.widgets)):
            self.active.append(True)
        for i in range(1,int((len(self.widgets)/2)+1)):
            self.positions.append([100,50*i+150])
            self.positions.append([300,50*i+150])
        
    #-- Botão de Iniciar
        IniciarLabel = Label(window)
        IniciarLabel.config(text="Simulate:", font=("arial", 12), bg = "grey")
        IniciarLabel.config(height = 2 , width = 20)
        IniciarLabel.place(x=labelx, y= 700)
        
        Iniciar = Button(window, text='Start', command=self.Start, bg="green")
        Iniciar.config(height=2, width=15)
        Iniciar.place(x=300, y= 700)
        
        self.startbuttom = Iniciar        
    #--- Current BID
        BIDLabel = Label(window)
        BIDLabel.config(text="Current BID:", font=("arial", 12), bg = "grey")
        BIDLabel.config(height = 2 , width = 15, borderwidth=2, relief="solid")
        BIDLabel.place(x=500, y= 20)
        
        BID = Label(window)
        BID.config(text="---", font=("arial", 12), bg = "grey")
        BID.config(height = 2 , width = 15, borderwidth=2, relief="solid")
        BID.place(x=500, y= 50)
        
        self.Bid.append(BIDLabel)
        self.Bid.append(BID)
    #--- Current ASK
        ASKLabel = Label(window)
        ASKLabel.config(text="Current ASK:", font=("arial", 12), bg = "grey")
        ASKLabel.config(height = 2 , width = 15, borderwidth=2, relief="solid")
        ASKLabel.place(x=650, y= 20)
        
        ASK = Label(window)
        ASK.config(text="---", font=("arial", 12), bg = "grey")
        ASK.config(height = 2 , width = 15, borderwidth=2, relief="solid")
        ASK.place(x=650, y= 50)
        
        self.Ask.append(ASKLabel) 
        self.Ask.append(ASK)
        
    #--- Number of trades dia       
        TradesLabel = Label(window)
        TradesLabel.config(text="Today Trades:", font=("arial", 12), bg = "grey")
        TradesLabel.config(height = 2 , width = 15, borderwidth=2, relief="solid")
        TradesLabel.place(x=800, y= 20)
        
        Trades = Label(window)
        Trades.config(text="---", font=("arial", 12), bg = "grey")
        Trades.config(height = 2 , width = 15, borderwidth=2, relief="solid")
        Trades.place(x=800, y= 50)
        
        self.Trades.append(TradesLabel) 
        self.Trades.append(Trades)
        
    #--- Number of trades total     
        TradesTLabel = Label(window)
        TradesTLabel.config(text="All Trades:", font=("arial", 12), bg = "grey")
        TradesTLabel.config(height = 2 , width = 15, borderwidth=2, relief="solid")
        TradesTLabel.place(x=950, y= 20)
        
        TradesT = Label(window)
        TradesT.config(text="---", font=("arial", 12), bg = "grey")
        TradesT.config(height = 2 , width = 15, borderwidth=2, relief="solid")
        TradesT.place(x=950, y= 50)
        
        self.TradesT.append(TradesTLabel) 
        self.TradesT.append(TradesT)
        
    #--- Current Total
        TotalLabel = Label(window)
        TotalLabel.config(text="Today Total:", font=("arial", 12), bg = "grey")
        TotalLabel.config(height = 2 , width = 15, borderwidth=2, relief="solid")
        TotalLabel.place(x=1100, y= 20)
        
        Total = Label(window)
        Total.config(text="---", font=("arial", 12), bg = "grey")
        Total.config(height = 2 , width = 15, borderwidth=2, relief="solid")
        Total.place(x=1100, y= 50)
        
        self.Total.append(TotalLabel) 
        self.Total.append(Total)
        
    #---Total Geral
        TotalGLabel = Label(window)
        TotalGLabel.config(text="All Total:", font=("arial", 12), bg = "grey")
        TotalGLabel.config(height = 2 , width = 15, borderwidth=2, relief="solid")
        TotalGLabel.place(x=1250, y= 20)
        
        TotalG = Label(window)
        TotalG.config(text="---", font=("arial", 12), bg = "grey")
        TotalG.config(height = 2 , width = 15, borderwidth=2, relief="solid")
        TotalG.place(x=1250, y= 50)
        
        self.TotalG.append(TotalGLabel) 
        self.TotalG.append(TotalG)
                
    def NameGraph(self):
        self.subplot[0].set_title('Model')
        self.subplot[0].set_xlabel('Ticks')
        self.subplot[0].set_ylabel('Value')
        
        self.subplot[1].set_title('Trades')
        self.subplot[1].set_xlabel('Ticks')
        self.subplot[1].set_ylabel('Value')
        
        self.subplot[2].set_title('Profit')
        self.subplot[2].set_xlabel('Ticks')
        self.subplot[2].set_ylabel('Value')
    
    def Graph(self, window, plt):
        
        self.fig = plt.Figure(figsize=(9,7), dpi=100)
        self.fig.subplots_adjust(hspace=0.5)
        self.subplot.append(self.fig.add_subplot(3,1,1))
        self.subplot.append(self.fig.add_subplot(3,1,2))
        self.subplot.append(self.fig.add_subplot(3,1,3))
        
        self.subplot[0].set_title('Model')
        self.subplot[0].set_xlabel('Ticks')
        self.subplot[0].set_ylabel('Value')
        
        self.subplot[1].set_title('Trades')
        self.subplot[1].set_xlabel('Ticks')
        self.subplot[1].set_ylabel('Value')
        
        self.subplot[2].set_title('Profit')
        self.subplot[2].set_xlabel('Ticks')
        self.subplot[2].set_ylabel('Value')
        
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        
        self.canvas = FigureCanvasTkAgg(self.fig, window)
        self.canvas.draw()
        self.canvas._tkcanvas.place(x=500,y=100)

    def Start(self):
        self.Runner = Runner()
        self.kill = False
        Erro = self.Debug()
        if not Erro:
            self.startbuttom.config(text="Stop", command=self.Stop, bg="red")
            #Cria lista de datas à analisar caso o range sejá marado (incompleto para anos diferentes)
            if self.variables[1].get():
                daysrange = []
                start = self.variables[0].get()
                end = self.variables[2].get()
                startyear, startmonth, startday = map(int, start.split("-"))
                endyear, endmonth, endday = map(int, end.split("-"))
                startmonthc, startdayc = startmonth, startday 
                endmonthc, enddayc = endmonth, endday
                for i in range(startyear, endyear+1):
                    startmonthc = startmonth
                    endmonthc = endmonth
                    if i != startyear and i != endyear:
                        startmonthc = 1
                        endmonthc = 12
                    elif i != endyear:
                        endmonthc = 12
                    elif i != startyear:
                        startmonthc = 1
                    for j in range(startmonthc, endmonthc+1):
                        startdayc = startday
                        enddayc = endday
                        if j != startmonth and j != endmonth:
                            startdayc = 1
                        elif j != endmonth:
                            enddayc = 31
                        elif j != startmonth:
                            startdayc = 1
                            
                        for k in range(startdayc, enddayc+1):
                            nday = k
                            nmonth = j
                            if k < 10:
                                nday = str(0) + str(k)
                            if j < 10:
                                nmonth = str(0) + str(j)
                            daysrange.append("{0}-{1}-{2}".format(i,nmonth,nday))
                            
            else:
                daysrange = [self.variables[0].get()]
                
            self.Source = Ticks(self.variables[3].get())
            self.Source.OpenData(daysrange, self.Data, self.DataPath)
            self.Source.Filtra()
            
            #--Define o modelo
            model = self.variables[4].get()
            
            if model == "Ticks Rolling Mean":
                from .Model import MMt
                self.Model = MMt(self.variables[5].get())
                self.ModelBoost = False
            elif model == "Time Rolling Mean":
                from .Model import MMT
                self.Model = MMT(self.variables[5].get())
                self.ModelBoost = False
            elif model == "Volume Adapt Rolling Mean":
                from .Model import MMVA
                self.Model = MMVA(self.variables[5].get())
                self.ModelBoost = False
            elif model == "Volume Rolling Mean":
                from .Model import MMV
                self.Model = MMV(self.variables[5].get())
                self.ModelBoost = False
            elif model == "Ticks Boost Rolling Mean":
                from .Model import MMt_Boost
                self.Model = MMt_Boost(self.variables[5].get())
                self.ModelBoost = True
                
                
            Signal = self.variables[6].get()
            #--Define o Broker
            if Signal != "No Trades":
                Broker = self.variables[8].get()
                
                if Broker == "Standard":
                    from .Broker import Broker_Standart
                    self.Broker = Broker_Standart()
                if Broker == "Waiter":
                    from .Broker import Broker_Waiter
                    self.Broker = Broker_Waiter()
            
            #--Define o sinal            
            if Signal == "Derivates (Alpha)":
                from .Signal import Signal_Derivates
                self.Signal = Signal_Derivates(self.variables[7].get(), self.variables[9].get(), self.Broker)
                self.SignalBoost = False
            elif Signal == "Derivates Boosted":
                from .Signal import Signal_Derivates_Boosted
                self.Signal = Signal_Derivates_Boosted(self.variables[7].get(), self.variables[9].get(), self.Broker)
                self.SignalBoost = True
                
            self.Ask[1].config(text="---")
            self.Bid[1].config(text="---")
            self.Trades[1].config(text="---")
            self.Total[1].config(text="---")
            
            if self.ModelBoost:    
                self.Runner.RunModelB(self, daysrange)
            elif self.SignalBoost:    
                self.Runner.RunBotB(self, daysrange) 
            elif self.SignalBoost and self.ModelBoost:
                self.Runner.RunAllB
            else:
                self.Runner.Runstd(self, daysrange)
        
    def Debug(self):
        Erro = False
        if self.variables[0].get() == "Select...":
            self.Debugprompt("No initial date selected")
            Erro = True
        if self.variables[1].get() and not Erro:
            if self.variables[2].get() == "Selecione...":
                self.Debugprompt("No ending date selected")
                Erro = True
            else:
                iniyear, inimonth, iniday = (self.variables[0].get()).split("-")
                endyear, endmonth, endday = (self.variables[2].get()).split("-")
                if iniyear > endyear:
                    self.Debugprompt("Initial date after ending date")
                    Erro = True
                elif iniyear == endyear:
                    if inimonth > endmonth:
                        self.Debugprompt("Initial date after ending date")
                        Erro = True
                    elif inimonth == endmonth:
                        if iniday > endday:
                            self.Debugprompt("Initial date after ending date")
                            Erro= True
                        elif iniday == endday:
                            self.Debugprompt("Initial date is the same as ending date")
                            Erro = True
        return Erro
                
    def Debugprompt(self, Errortext):
        win = Toplevel()
        win.wm_title("Warning")
        
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry('{}x{}+{}+{}'.format(200, 50, x, y))
        win.columnconfigure(0, weight=1)
        win.attributes('-topmost', 'true')
        
        error = Label(win, text=Errortext)
        error.grid(row=0, column=0)
    
        ok = Button(win, text="Understood", command=win.destroy)
        ok.grid(row=1, column=0)
        
        
    def Debugdayend(self):
        win = Toplevel()
        win.wm_title("Warning")
        
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry('{}x{}+{}+{}'.format(200, 50, x, y))
        win.columnconfigure(0, weight=1)
        win.attributes('-topmost', 'true')
        
        error = Label(win, text="Starting Next Day")
        error.grid(row=0, column=0)
    
        ok = Button(win, text="Understood", command=win.destroy)
        ok.grid(row=1, column=0)
        
    def Debugprogramend(self):
        win = Toplevel()
        win.wm_title("Warning")
        
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry('{}x{}+{}+{}'.format(200, 50, x, y))
        win.columnconfigure(0, weight=1)
        win.attributes('-topmost', 'true')
        
        error = Label(win, text="Program Done")
        error.grid(row=0, column=0)
    
        ok = Button(win, text="Understood", command=win.destroy)
        ok.grid(row=1, column=0)
        
    def Stop(self):
        self.kill = True
        self.startbuttom.config(text="Start", command=self.Start, bg="green")
        
        