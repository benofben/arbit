function [prediction, truePositive, falsePositive, accuracy] = predictor1(b_margin)
%PREDICTOR1 Summary of this function goes here
% going to try beta...
load b

fprintf('Building predictor 1 (beta) for margin %f.\n', b_margin);

symbols = textread('C:\momentum\data\symbols\successfullyReformattedSymbols.txt', '%s');
    
falsePositive=0;
truePositive=0;
total=0;

for symbolIndex=1:size(symbols,1)
    fprintf('Building predictor 1 for symbol %s for beta %f.\n', symbols{symbolIndex}, b_margin);
    symbol=symbols{symbolIndex};
    filename = strcat('C:\momentum\data\train\', symbol, '.csv');
    stock=load(filename);

    openPrice=stock(:,2);
    highPrice=stock(:,3);
    lowPrice=stock(:,4);
    closePrice=stock(:,5);
    
    % for each training example
    for time=1:size(openPrice,1)
                
        if(b(symbolIndex)>b_margin && highPrice(time)>openPrice(time)*1.02)
            truePositive=truePositive+1;
        elseif(b(symbolIndex)>b_margin && highPrice(time)<openPrice(time)*1.02)
            falsePositive=falsePositive+1;
        end
        total=total+1;
    end
end

truePositive=truePositive/total;
falsePositive=falsePositive/total;
accuracy=truePositive/(truePositive+falsePositive);