function [prediction, truePositive, falsePositive, accuracy] = predictor2(window)
%PREDICTOR2 Summary of this function goes here
%  predictor 2 is p((high-open)/open) for the last time window for a stock
%  this predictor is a function of a symbol and a time

fprintf('Building predictor 2 for window %i.\n', window);
symbols = textread('C:\momentum\data\symbols\successfullyReformattedSymbols.txt', '%s');
    
falsePositive=0;
truePositive=0;
total=0;

for symbolIndex=1:size(symbols,1)
%    fprintf('Building predictor 2 for symbol %s with window %i.\n', symbols{symbolIndex}, window);
    symbol=symbols{symbolIndex};
    filename = strcat('C:\momentum\data\train\', symbol, '.csv');
    stock=load(filename);

    openPrice=stock(:,2);
    highPrice=stock(:,3);
    lowPrice=stock(:,4);
    closePrice=stock(:,5);
    
    % for each training example
    for time=window+1:size(openPrice,1)
        
        % for the time window
        pGoodDay(symbolIndex, time-window)=0;
        for t=time-window:time-1
            if(highPrice(t)>openPrice(t)*1.02)
                pGoodDay(symbolIndex, time-window) = pGoodDay(symbolIndex, time-window)+1;
            end
        end
        pGoodDay(symbolIndex, time-window)=pGoodDay(symbolIndex, time-window)/window;
        
        if(pGoodDay(symbolIndex, time-window)>0.7 && highPrice(time)>openPrice(time)*1.02)
            truePositive=truePositive+1;
        elseif(pGoodDay(symbolIndex, time-window)>0.7 && highPrice(time)<openPrice(time)*1.02)
            falsePositive=falsePositive+1;
        end
        total=total+1;
    end
end

truePositive=truePositive/total;
falsePositive=falsePositive/total;
accuracy=truePositive/(truePositive+falsePositive);
prediction=pGoodDay;