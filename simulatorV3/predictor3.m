function [pGoodDay, truePositive, falsePositive] = predictor3()
%PREDICTOR3 Summary of this function goes here
%  predictor 3 is (high-open)/open for the last week
%  this is l1, for t-1.  It doesn't work, don't use it!!!!!!

symbols = textread('C:\momentum\data\symbols\successfullyReformattedSymbols.txt', '%s');

% this is the probability that the metric was correct over all examples
truePositive=0;
falsePositive=0;
total=0;

for symbolIndex=1:size(symbols,1)
    fprintf('Building predictor 3 for symbol %s.\n', symbols{symbolIndex});
    symbol=symbols{symbolIndex};
    filename = strcat('C:\momentum\data\train\', symbol, '.csv');
    stock=load(filename);

    openPrice=stock(:,2);
    highPrice=stock(:,3);
    lowPrice=stock(:,4);
    closePrice=stock(:,5);
    
    % for each training example
    for time=2:size(openPrice,1)
        
        % for the time window
        if(highPrice(time-1)>openPrice(time-1)*1.02)
            pGoodDay(symbolIndex, time-1) = 1;
        else
            pGoodDay(symbolIndex, time-1) = 0;
        end
        
        if(pGoodDay(symbolIndex, time-1)==1 && highPrice(time)>openPrice(time)*1.02)
            truePositive=truePositive+1;
        elseif(pGoodDay(symbolIndex, time-1)==1 && highPrice(time)<openPrice(time)*1.02)
            falsePositive=falsePositive+1;
        end
        total=total+1;
    end
end
truePositive=truePositive/total;
falsePositive=falsePositive/total;