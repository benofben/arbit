clear all

symbols = textread('C:\momentum\data\symbols\successfullyReformattedSymbols.txt', '%s');

rate=1.02;

% need to find out how much data we have...
symbol='BEAS';
filename = strcat('C:\momentum\data\train\', symbol, '.csv');
stock=load(filename);
openPrice=stock(:,2);

capital=25000;

time=size(openPrice,1);
p1 = predictor1(symbols, time);
p2 = predictor2(symbols, time);
p3 = predictor3(symbols, time);
    
% create a joint variable p
for symbolIndex=1:size(p1,2)
    p(symbolIndex)=(1-p1(symbolIndex))*(1-p2(symbolIndex))*(1-p3(symbolIndex));
    p(symbolIndex)=1-p(symbolIndex);
end
    
% now sort on p
prows(:,1)=transpose(p);
prows(:,2)=transpose(p1);
prows(:,3)=transpose(p2);
prows(:,4)=transpose(p3);
[prows, symbolIndex]=sortrows(prows);
prows(:,5)=symbolIndex;