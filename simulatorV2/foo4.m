clear all
symbols = textread('C:\momentum\data\symbols\successfullyReformattedSymbols.txt', '%s');

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

        percentReturn(i)=1;
        for t=1:size(openPrice,1)
            if(highPrice(t)>openPrice(t)*1.02)
                percentReturn(i)=percentReturn(i)*1.02;
            else
                badDay=(closePrice(t)-openPrice(t))/openPrice(t);
                percentReturn(i)=percentReturn(i)*(1+badDay);
            end
        end
    end

    % test
    while(1==1)
        [y,i]=max(percentReturn);
        symbol=symbols{i};

        filename = strcat('C:\momentum\data\train\', symbol, '.csv');
        stock=load(filename);

        openPrice=stock(:,2);
        highPrice=stock(:,3);
        lowPrice=stock(:,4);
        closePrice=stock(:,5);
        volume=stock(:,6);

        if(volume(time-1)>(capital/openPrice(time))*100)
		break
        end

        % otherwise the stock doesn't have sufficient volume for our purposes
        % so, we mark its return as 0
        percentReturn(i)=0;
    end

    if(highPrice(time)>openPrice(time)*1.02)
        capital=capital*1.02;
    else
        badDay=(closePrice(time)-openPrice(time))/openPrice(time);
        capital=capital*(1+badDay);
    end
    
    fid = fopen('C:\momentum\data\foo2.csv','a');
    fprintf(fid, '%i, %s, %f, %i\n', time, symbols{i}, percentReturn(i), capital);
    fclose(fid);
    
    fprintf('Picked %s at time %i, giving $%i.\n', symbols{i}, time, capital);
    
end