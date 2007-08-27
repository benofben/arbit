clear all
load b
symbols = textread('C:\momentum\data\symbols\successfullyReformattedSymbols.txt', '%s');

p01GoodDay=zeros(size(symbols,1),1);
p02GoodDay=zeros(size(symbols,1),1);

for i=1:size(symbols,1)
    symbol=symbols{i};

    fprintf('Processing symbol %s\n', symbol);
    filename = strcat('C:\momentum\data\train\', symbol, '.csv');
    stock=load(filename);

    % withhold a testing set
    stock = stock(1:floor(size(stock,1)/2),:);
    
    openPrice=stock(:,2);
    highPrice=stock(:,3);
    lowPrice=stock(:,4);
    closePrice=stock(:,5);

    j01=1;
    j02=1;
    clear badDay01;
    clear badDay02;

    capital01(i)=25000;
    capital02(i)=25000;
    for time=1:size(openPrice,1)/2
        l1(time)=(highPrice(time)-openPrice(time))/openPrice(time);

        if(l1(time)>0.02)
            p02GoodDay(i)=p02GoodDay(i)+1;
            capital02(i)=capital02(i)*1.02;
        else
            badDay02(j02)=(closePrice(time)-openPrice(time))/openPrice(time);
            capital02(i)=capital02(i)*(1+badDay02(j02));
            j02=j02+1;
        end
        
        if(l1(time)>0.01)
            p01GoodDay(i)=p01GoodDay(i)+1;
            capital01(i)=capital01(i)*1.01;
        else
            badDay01(j01)=(closePrice(time)-openPrice(time))/openPrice(time);
            capital01(i)=capital01(i)*(1+badDay01(j01));
            j01=j01+1;
        end
        
    end
    p01GoodDay(i)=p01GoodDay(i)/size(openPrice,1);
    p02GoodDay(i)=p02GoodDay(i)/size(openPrice,1);

    muBadDay01(i)=mean(badDay01);
    stdBadDay01(i)=std(badDay01);
    
    muBadDay02(i)=mean(badDay02);
    stdBadDay02(i)=std(badDay02);
    
    mu=mean(l1);
    sigma=std(l1);
    lambda(i)=1/((mu+sigma)/2);
end