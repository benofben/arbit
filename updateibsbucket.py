import quotes

symbols=['C','CS','DB','GS','LEH','MER','RY','UBS','WB', 'HBC']
# 'HBC','AIG'

for symbol in symbols:
    quotes.downloadQuotes(symbol)
