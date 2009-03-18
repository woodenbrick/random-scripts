import wx
import random

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='Game', size=(600, 600))
        self.statusBar = self.CreateStatusBar()
        self.statusBar.SetOwnFont(wx.Font(10, 1, 1, 1))
        self.panel = GamePanel(self)
        #menus
        fileMenu = wx.Menu()
        fileMenu.Append(23, 'New Game', 'Start a new game')
        fileMenu.Append(24, 'Change Player')
        fileMenu.AppendSeparator()
        fileMenu.Append(25, 'Exit')
        
        menubar = wx.MenuBar()
        menubar.Append(fileMenu, 'File')
        
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.newGame, id=23)
        self.Bind(wx.EVT_MENU, self.changePlayer, id=24)
        self.Bind(wx.EVT_MENU, self.exit, id=25)
        
        
        
    def newGame(self, event):
        self.panel.clickOrder = []
        self.panel.clickCount = 0
        random.shuffle(self.panel.numbers)
        i=1
        print self.panel.numbers
        for n in self.panel.numbers:
            self.FindWindowById(i).Enable()
            self.FindWindowById(i).SetBackgroundColour('White')
            self.FindWindowById(i).setNumber(n)
            i+=1



    
    def changePlayer(self, event):
        pass



    
    def exit(self, event):
        print 'closing'
        self.Close()
        
        

class GamePanel(wx.Panel):
    def __init__(self, frame):
        wx.Panel.__init__(self, frame)
        self.frame = frame
        self.SetFont(wx.Font(30, 1, 1, 1))
        self.numbers = range(1, 17)
        self.clickOrder = []
        self.clickCount = 0
        random.shuffle(self.numbers)
        
        topSizer = wx.BoxSizer()
        midSizer = wx.BoxSizer()
        botSizer = wx.BoxSizer()
        nextBot = wx.BoxSizer()
        buttonSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer = wx.BoxSizer()
        i=1
        for n in self.numbers:
            button = self.createButton(n, i)
            if i < 5:
                topSizer.Add(button, 1, wx.EXPAND)
            elif i > 4 and i < 9:
                midSizer.Add(button, 1, wx.EXPAND)
            elif i > 8 and i < 13:
                botSizer.Add(button, 1, wx.EXPAND)
            else:
                nextBot.Add(button, 1, wx.EXPAND)
            i+=1
            
        #feedback area
        #self.feedback = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        buttonSizer.Add(topSizer, 1, wx.EXPAND)
        buttonSizer.Add(midSizer, 1, wx.EXPAND)
        buttonSizer.Add(botSizer, 1, wx.EXPAND)
        buttonSizer.Add(nextBot, 1, wx.EXPAND)
        mainSizer.Add(buttonSizer, 1, wx.EXPAND)
        #mainSizer.Add(self.feedback, 1, wx.EXPAND)
        self.SetSizer(mainSizer)
        
        #menus
        
        
        





    def onClick(self, event):
        '''disables the button clicked and appends it to the clicked list'''
        id = event.GetId()
        self.FindWindowById(id).Disable()
        self.FindWindowById(id).SetBackgroundColour('Grey')
        self.clickOrder.append(self.FindWindowById(id).buttonNumber)
        self.clickCount +=1
        if self.clickCount == 1:
            for i in range(1, 17):
                self.FindWindowById(i).SetLabel('')
        if self.clickCount == 9:
            
            #put the numbers back up
            fback = 'Results:'
            res = self.getResults()
            fback += str(100 - (len(res) * 10)) + '% correct' 
            for id in range(1, 17):
                self.FindWindowById(id).showNumber()
                value = self.FindWindowById(id).returnNumber()
                if res.__contains__(value):
                    self.FindWindowById(id).SetBackgroundColour('Red')
                else:
                    self.FindWindowById(id).SetBackgroundColour('Green')

            self.frame.statusBar.SetStatusText(fback)
                
                



   




   
    def createButton(self, text, ident):
        
        class labelButton(wx.Button):
            def __init__(self, text, parent):
                self.buttonNumber = text
                wx.Button.__init__(self, parent=parent, label=str(self.buttonNumber), id=ident)
                self.SetBackgroundColour('White')
                if self.buttonNumber > 9:
                    self.SetLabel('')
                
            def setNumber(self, newName):
                self.buttonNumber = newName
                if newName < 10:
                    self.SetLabel(str(self.buttonNumber))
                else:
                    self.SetLabel('')
                    
            def showNumber(self):
                if self.buttonNumber < 10:
                    self.SetLabel(str(self.buttonNumber))
                
            def returnNumber(self):
                return self.buttonNumber
        
        b = labelButton(text, self)
        b.Bind(wx.EVT_BUTTON, self.onClick)
        return b



    
    def getResults(self):
        incorrect = []
        i = 1
        for guess in self.clickOrder:
            if guess != i:
                incorrect.append(guess)
            i+=1
        return incorrect



    

app = wx.App()
fr = MainFrame()
fr.Show()
app.MainLoop()
    