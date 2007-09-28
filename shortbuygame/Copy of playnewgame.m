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

    buyPrice=openPrice(time)*0.99;
    sellPrice=openPrice(time)*1.01;
    
    if(lowPrice(time)<=buyPrice && highPrice(time)>=sellPrice)
        % win
        shares=capital(time)/buyPrice;
        capital(time)=shares*sellPrice;
    elseif(lowPrice(time)>buyPrice && highPrice(time)>=sellPrice)
        % lose, we went long at +1, and sold at close
        shares=capital(time)/buyPrice;
        capital(time)=shares*closePrice(time);
    elseif(lowPrice(time)<=buyPrice && highPrice(time)<sellPrice)
        % lose, we sold at +1
        shares=capital(time)/buyPrice;
        capital(time)=shares*closePrice(time);
    else
        % don't play
    end
end
plot(capital(1:50));