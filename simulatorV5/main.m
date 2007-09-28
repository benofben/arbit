clear all;
symbols = textread('C:\momentum\data\symbols\successfullyReformattedSymbols.txt', '%s');

fprintf('Loading data.');
i=1;
for symbolIndex=1:size(symbols,1)
    filename = strcat('C:\momentum\data\train\', symbols{symbolIndex}, '.csv');
    stock=load(filename);
    
    % traded on nasdaq
    if(size(stock(:,2),1)==705)
        openPrice(:,i)=stock(:,2);
        highPrice(:,i)=stock(:,3);
        lowPrice(:,i)=stock(:,4);
        closePrice(:,i)=stock(:,5);
        i=i+1;
    end
end

fprintf('Beginning simulation...\n')
capital(1:size(openPrice,1))=25000;

fid = fopen('predictions.csv','w');

for time=40:size(openPrice,1)/2
    fprintf('Simulating time %i.\n', time);
    capital(time)=capital(time-1);
    
    prediction3 = predictor3(...
        openPrice(time-39:time-1,:), ...
        highPrice(time-39:time-1,:), ...
        closePrice(time-39:time-1,:));
        
    for symbolIndex=1:size(openPrice,2)
        prediction1(symbolIndex) = predictor1(symbolIndex);
        prediction2(symbolIndex) = predictor2(...
            openPrice(time-39:time-1,symbolIndex), ...
            highPrice(time-39:time-1,symbolIndex), ...
            closePrice(time-39:time-1,symbolIndex));
    end
        
    [y,i]=max(prediction2);
    
    if(highPrice(time, i)>openPrice(time,i)*1.02)
        capital(time)=capital(time)*1.02;
    else
        a=1+(closePrice(time,i)-openPrice(time,i))/openPrice(time,i);
        capital(time)=capital(time)*a;
    end
    
    fprintf(fid, '%i, %f, %f, %f, %s, %f\n', time, prediction1(i), prediction2(i), prediction3(i), symbols{i}, capital(time));
end
fclose(fid);

h=plot(capital);
xlabel='Day';
ylabel='Capital';
saveas(h, 'capital.jpg', 'jpg');