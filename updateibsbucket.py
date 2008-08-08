import quotes

symbols=['C','CS','DB','GS','LEH','MER','RY','UBS','WB','HBC']#'JPM','BAC','WFC','WM','AIG']

for symbol in symbols:
    quotes.downloadQuotes(symbol)
