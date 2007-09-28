function prediction = predictor3(openPrice, highPrice, closePrice)
%PREDICTOR2 Summary of this function goes here
%  predictor 2 is p((high-open)/open) for the last time window for a stock
%  this predictor is a function of a time window, incorporating data from
%  the entire market.

win=0;
lose=0;
total=0;
for time=1:size(openPrice,1)
    for symbolIndex=1:size(openPrice,2)
        if(highPrice(time, symbolIndex)>openPrice(time, symbolIndex)*1.02)
            win=win+1;
        else
            lose=lose+1;
        end
        total=total+1;
    end
end

if(total~=0 && win+lose~=0)
    winRate=win/total;
    loseRate=lose/total;
    prediction=winRate/(winRate+loseRate);
else
    prediction=0;
end