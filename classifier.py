# for maxint
import sys
import data

classes=['Good', 'Bad']

class classifier:
    def __init__(self, symbol, currentDate, quotes):
        self.symbol=symbol
        self.currentDate=currentDate
        self.quotes=quotes

    def run(self):
        dataSet=self.createDataSet()

        # compute P(C|F_1, F_2, ... F_n)
        if dataSet and len(dataSet)>1:
            testPoint=dataSet[-1]

            p={}
            for C in classes:

                # compute p(C)
                p[C]=0
                for day in range(0, len(dataSet)-1):
                    if dataSet[day]['Outcome']==C:
                        p[C]=p[C]+1.0
                p[C]=p[C]/(len(dataSet)-1)
                
                # compute p(F_i|C)

                # there has got to be a better way to do this....
                pF=[]
                Ft=[]
                for i in dataSet[0]:
                    if i!='Outcome':
                        for j in range(0,len(dataSet[0][i])):
                            pF.append(0)
                            Ft.append(0)

                for day in range(0, len(dataSet)-1):
                    if dataSet[day]['Outcome']==C:
                        index=0
                        for i in dataSet[day]:
                            if i!='Outcome':
                                for j in range(0,len(dataSet[day][i])):
                                    if dataSet[day][i][j]==testPoint[i][j]:
                                        pF[index]=pF[index]+1
                                    Ft[index]=Ft[index]+1
                                    index=index+1

                # compute p(C|F_1,...F_n) = p(C) * Pi[p(F_i|C)]
                for i in range(0,len(pF)):
                    if pF[i]!=0:
                        pF[i]=float(pF[i])/Ft[i]
                    else:
                        pF[i]=0.01
                    p[C]=p[C]*pF[i]

            # scale p(C) by 1/Z
            Z=0
            for C in p:
                Z=Z+p[C]
            for C in p:
                p[C]=p[C]/Z
            return p
        return False

    def createDataPoint(self, day, symbol):
        # add the symbol
        dataPoint={}
        dataPoint['Symbol']=[]
        dataPoint['Symbol'].append(self.quotes[symbol])

        '''
        # populate the Window Predictors for today
        dataPoint['WindowPredictor']=[]
        window=3
        for index in range(day-window, day):
            if self.subquote[symbol]['High'][index]>self.subquote[symbol]['Open'][index]*1.02:
                dataPoint['WindowPredictor'].append(1.02)
            else:
                binned = self.bin(self.subquote[symbol]['Close'][index]/self.subquote[symbol]['Open'][index])
                dataPoint['WindowPredictor'].append(binned)
        '''

        # last closing price was x% of the y day high, low
        High=0
        Low=sys.maxint
        for i in range(day-5, day):
            if self.quotes[symbol]['High'][i]>High:
                High=self.quotes[symbol]['High'][i]
            if self.quotes[symbol]['Low'][i]<Low:
                Low=self.quotes[symbol]['Low'][i]
        dataPoint['xDay']=[]
        Last=self.quotes[symbol]['Close'][day]
        dataPoint['xDay'].append(self.bin(Last/High))
        dataPoint['xDay'].append(self.bin(Last/Low))

        # populate the outcome for today
        if self.quotes[symbol]['High'][day]>self.quotes[symbol]['Open'][day]*1.02:
            dataPoint['Outcome']='Good'
        else:
            dataPoint['Outcome']='Bad'

        return dataPoint

    def createDataSet(self):
        trainingWindow=100
        dataSet=[]
        for symbol in self.quotes:
            currentIndex=data.getIndex(self.currentDate, self.quotes[symbol])
            if currentIndex and currentIndex-trainingWindow-5>0:
                for day in range(currentIndex-trainingWindow, currentIndex):
                    dataSet.append(self.createDataPoint(day, symbol))

        #now append the test point
        day=data.getIndex(self.currentDate, self.quotes[self.symbol])
        dataSet.append(self.createDataPoint(day, self.symbol))
                       
        return dataSet

    def bin(self, x):
        return round(x*20)/20
