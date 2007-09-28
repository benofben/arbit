clear all;
wekaOut = load ('../data/matlab/BEASOut.csv');
testCSV = load('../data/matlab/testBEAS.csv');
quotes = load('../data/train/BEAS.csv');

testIndex=size(quotes,1)-size(testCSV,1)+1;
quotes=quotes(testIndex:size(quotes,1),:);

openPrice=quotes(:,2);
highPrice=quotes(:,3);
closePrice=quotes(:,5);

capital=25000;
for day=2:size(wekaOut,1)
    capital(day)=capital(day-1);
    
    if(wekaOut(day,2)==1) %then buy
        shares=capital(day)/openPrice(day);
        capital(day)=0;
        
        if(highPrice(day)>openPrice(day)*1.02)
            capital(day)=shares*openPrice(day)*1.02;
        else
            capital(day)=shares*closePrice(day);
        end
    end
end


%plot(capital(1,250))
plot(capital)
xlabel('wasted days')
ylabel('probability of an idle life in Paris')