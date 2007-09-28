symbol='BEAS';
filename = strcat('C:\momentum\data\train\', symbol, '.csv');
stock=load(filename);

openPrice=stock(:,2);
highPrice=stock(:,3);
lowPrice=stock(:,4);
closePrice=stock(:,5);
    
% play the margin game
capital=25000;
% for each training example
for time=2:size(openPrice,1)
    capital(time)=capital(time-1);

    buyPrice=openPrice(time)*0.95;
    
    if(lowPrice(time)<buyPrice)
        shares=capital(time)/buyPrice;
        capital(time)=shares*closePrice(time);        
    end
end
plot(capital);