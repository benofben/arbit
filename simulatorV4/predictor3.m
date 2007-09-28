%%%%%%%%%%%%%%%% this is all fucked up because it doesn't take into account
%%%%%%%%%%%%%%%% markets open for different numbers of
%%%%%%%%%%%%%%%% days!!!!!!!!!!!!!!!!!!

%function [prediction, truePositive, falsePositive, accuracy] = predictor3(window)
%PREDICTOR2 Summary of this function goes here
%  predictor 2 is p((high-open)/open) for the last time window
%  this predictor is a function of time (uses l1 for the entire market
%  unlike predictor 2

fprintf('Building predictor 3 for window %i.\n', window);
symbols = textread('C:\momentum\data\symbols\successfullyReformattedSymbols.txt', '%s');
    
falsePositive=0;
truePositive=0;
total=0;

% need to find out how much stock data we have to instantiate pGoodDay
filename = strcat('C:\momentum\data\train\', 'F', '.csv');
stock=load(filename);
openPrice=stock(:,2);
pGoodDay=zeros(size(openPrice,1)-window,1);

% build the predictor
for symbolIndex=1:size(symbols,1)
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
        for t=time-window:time-1
            if(highPrice(t)>openPrice(t)*1.02)
                pGoodDay(time-window) = pGoodDay(time-window)+1;
            end
        end
    end
end

for time=window+1:size(openPrice,1)
    pGoodDay(time-window)=pGoodDay(time-window)/(window*size(symbols,1));
end

% now let's test our predictor
for symbolIndex=1:size(symbols,1)
    symbol=symbols{symbolIndex};
    filename = strcat('C:\momentum\data\train\', symbol, '.csv');
    stock=load(filename);

    openPrice=stock(:,2);
    highPrice=stock(:,3);
    lowPrice=stock(:,4);
    closePrice=stock(:,5);

    % for each training example
    for time=window+1:size(openPrice,1)

        if(pGoodDay(time-window)>0.5 && highPrice(time)>openPrice(time)*1.02)
            truePositive=truePositive+1;
        elseif(pGoodDay(time-window)>0.5 && highPrice(time)<openPrice(time)*1.02)
            falsePositive=falsePositive+1;
        end
        total=total+1;
    end
end

truePositive=truePositive/total;
falsePositive=falsePositive/total;
accuracy=truePositive/(truePositive+falsePositive);
prediction=pGoodDay;