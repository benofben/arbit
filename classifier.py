classes=["Very Good", "Good", "Bad", "Very Bad"]

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
                    if dataSet[day]["Outcome"]==C:
                        p[C]=p[C]+1.0
                p[C]=p[C]/(len(dataSet)-1)
                
                # compute p(F_i|C)

                # there has got to be a better way to do this....
                pF=[]
                Ft=[]
                for i in range(0,len(dataSet[0]["Predictor"])):
                    pF.append(0)
                    Ft.append(0)

                for day in range(0, len(dataSet)-1):
                    if dataSet[day]["Outcome"]==C:
                        for i in range(0,len(dataSet[day]["Predictor"])):
                            if dataSet[day]["Predictor"][i]==testPoint["Predictor"][i]:
                                pF[i]=pF[i]+1
                            Ft[i]=Ft[i]+1

                # compute p(C|F_1,...F_n) = p(C) * Pi[p(F_i|C)]
                for i in range(0,len(pF)):
                    if pF[i] !=0:
                        pF[i]=float(pF[i])/Ft[i]
                    else:
                        pF[i]=0.01
                    p[C]=p[C]*pF[i]

            #scale p(C) by 1/Z
            Z=0
            for C in classes:
                Z=Z+p[C]
            for C in classes:
                p[C]=p[C]/Z

            p['dataLength']=len(dataSet)
            return p
        return False
    
    def createDataSet(self):
        window=90
        dataSet=[]
        for symbol in self.subquote:
            for day in range(window, len(self.subquote[symbol]["Open"])+1):
                dataSet.append({})

                # populate the predictors for today
                dataSet[day-window]["Predictor"]=[]
                for index in range(day-window, day):
                    if self.subquote[symbol]["High"][index]>self.subquote[symbol]["Open"][index]*1.02:
                        dataSet[day-window]["Predictor"].append(1.02)
                    else:
                        binned = self.bin(self.subquote[symbol]["Close"][index]/self.subquote[symbol]["Open"][index])
                        dataSet[day-window]["Predictor"].append(binned)

                # populate the outcome for today
                if day<len(self.subquote[symbol]["Open"]):
                    if self.subquote[symbol]["High"][day]>self.subquote[symbol]["Open"][day]*1.02:
                        dataSet[day-window]["Outcome"]="Very Good"
                    elif self.subquote[symbol]["Close"][day]>self.subquote[symbol]["Open"][day]:
                        dataSet[day-window]["Outcome"]="Good"
                    elif self.subquote[symbol]["Close"][day]>self.subquote[symbol]["Open"][day]*0.98:
                        dataSet[day-window]["Outcome"]="Bad"
                    else:
                        dataSet[day-window]["Outcome"]="Very Bad"

        return dataSet

    def bin(self, x):
        return round(x*100)/100
