clear all
load b
symbols = textread('C:\momentum\data\symbols\successfullyReformattedSymbols.txt', '%s');

rate=1.02;

% need to find out how much data we have...
symbol='BEAS';
filename = strcat('C:\momentum\data\train\', symbol, '.csv');
stock=load(filename);
openPrice=stock(:,2);

capital=25000;

% delete the existing file
fid = fopen('C:\momentum\data\foo2.csv','w');
fclose(fid);

for time=243:size(openPrice,1)
    
    % train
    for i=1:size(symbols,1)
        symbol=symbols{i};

        filename = strcat('C:\momentum\data\train\', symbol, '.csv');
        stock=load(filename);

        % delete what we aren't training with
        stock = stock(time-242:time-1,:);

        openPrice=stock(:,2);
        highPrice=stock(:,3);
        lowPrice=stock(:,4);
        closePrice=stock(:,5);

        % compute annual statistic
        annualPercentReturn(i)=1;
        for t=1:size(openPrice,1)
            if(highPrice(t)>openPrice(t)*rate)
                annualPercentReturn(i)=annualPercentReturn(i)*rate;
            else
                badDay=(closePrice(t)-openPrice(t))/openPrice(t);
                annualPercentReturn(i)=annualPercentReturn(i)*(1+badDay);
            end
        end
        %annualPercentReturn(i)=exp(log(annualPercentReturn(i))/242);
         
        % compute weekly statistic
        weekPercentReturn(i)=1;
        for t=size(openPrice,1)-6:size(openPrice,1)
            if(highPrice(t)>openPrice(t)*rate)
                weekPercentReturn(i)=weekPercentReturn(i)*rate;
            else
                badDay=(closePrice(t)-openPrice(t))/openPrice(t);
                weekPercentReturn(i)=weekPercentReturn(i)*(1+badDay);
            end
        end
        weekPercentReturn(i)=exp(log(weekPercentReturn(i))/5);

    end

    % test
    while(1==1)
        [y,i]=max(annualPercentReturn+weekPercentReturn);
        symbol=symbols{i};

        filename = strcat('C:\momentum\data\train\', symbol, '.csv');
        stock=load(filename);

        openPrice=stock(:,2);
        highPrice=stock(:,3);
        lowPrice=stock(:,4);
        closePrice=stock(:,5);
        volume=stock(:,6);

        % l1
        l1=(highPrice(time-1)-openPrice(time-1))/openPrice(time-1);
        
        %dailyReturn1
        dailyReturn1=(closePrice(time-2)-closePrice(time-1))/closePrice(time-1);
        
        %tradingDayReturn1
        tradingDayReturn1=(closePrice(time-1)-openPrice(time-1))/openPrice(time-1);

        if(volume(time-1)>(capital/openPrice(time))*100)
%            if(b(i)>2)
%            if(l1<0.08 || dailyReturn1>-0.06 || tradingDayReturn1<0.08)
                break
        end
                
        % otherwise the stock didn't satisfy one of our conditions
        % so, we mark its return as 0
        annualPercentReturn(i)=0;
        weekPercentReturn(i)=0;
    end

    if(highPrice(time)>openPrice(time)*rate)
        capital=capital*rate;
    else
        badDay=(closePrice(time)-openPrice(time))/openPrice(time);
        capital=capital*(1+badDay);
    end
    
    fid = fopen('C:\momentum\data\foo2.csv','a');
    fprintf(fid, '%i, %s, %f, %f, %i\n', time, symbols{i}, annualPercentReturn(i), weekPercentReturn(i), capital);
    fclose(fid);
    
    fprintf('Picked %s at time %i, giving $%i.\n', symbols{i}, time, capital);
    
end