function ra = computePercentChange(r)
%computePercentChange Computes the percent change for a time series array.

ra=zeros(size(r));
ra(1,1)=1;
for(i=1:size(r,1)-1)
    ra(i+1,1)=r(i+1,1)/r(i,1);
end

return;