import sys
classes=['Good', 'Bad']

class classifier:
    def __init__(self, subquote):
        self.subquote=subquote

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
    
    def createDataSet(self):
        trainingWindow=100
        dataSet=[]
        for symbol in self.subquote:
            days = len(self.subquote[symbol]['Open'])
            if days-trainingWindow-242>0:
                for day in range(days-trainingWindow, days):
                    dataSet.append({})

                    '''
                    # populate the Window Predictors for today
                    dataSet[-1]['WindowPredictor']=[]
                    window=3
                    for index in range(day-window, day):
                        if self.subquote[symbol]['High'][index]>self.subquote[symbol]['Open'][index]*1.02:
                            dataSet[-1]['WindowPredictor'].append(1.02)
                        else:
                            binned = self.bin(self.subquote[symbol]['Close'][index]/self.subquote[symbol]['Open'][index])
                            dataSet[-1]['WindowPredictor'].append(binned)
                    '''
                    
                    # last closing price was x% of the 1 year high, low
                    High=0
                    Low=sys.maxint
                    for i in range(day-242, day):
                        if self.subquote[symbol]['High'][i]>High:
                            High=self.subquote[symbol]['High'][i]
                        if self.subquote[symbol]['Low'][i]<Low:
                            Low=self.subquote[symbol]['Low'][i]
                    dataSet[-1]['52Week']=[]
                    Last=self.subquote[symbol]['Close'][day]
                    dataSet[-1]['52Week'].append(self.bin(Last/High))
                    dataSet[-1]['52Week'].append(self.bin(Last/Low))

                    # populate the outcome for today
                    if self.subquote[symbol]['High'][day]>self.subquote[symbol]['Open'][day]*1.02:
                        dataSet[-1]['Outcome']='Good'
                    else:
                        dataSet[-1]['Outcome']='Bad'

        return dataSet

    def bin(self, x):
        return round(x*20)/20
