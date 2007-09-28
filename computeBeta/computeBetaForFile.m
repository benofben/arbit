function b = computeBetaForFile(symbol)
%BETA Compute the beta for a set of observations contained in a file

market=load('C:\momentum\data\reformattedQuotes\VTI.csv');
filename = strcat('C:\momentum\data\train\', symbol, '.csv');
stock=load(filename);

market_adj_close=zeros(size(stock(:,7)));
for i=1:size(stock,1)
    for j=1:size(market,1)
        if stock(i,1)==market(j,1)
            market_adj_close(i,1)=market(j,7);
        end
    end
end

stock_adj_close = stock(:,7);

%market
rp = computePercentChange(market_adj_close);

%stock
ra = computePercentChange(stock_adj_close);

b = beta(ra,rp);