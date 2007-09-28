function b = beta(ra,rp)

% this is bad.  Something's fucked with the logic in here.  var(rp)=0?
warning off MATLAB:divideByZero

%BETA Compute the beta for a set of observations
betaMatrix=cov(rp,ra)/var(rp);
b=betaMatrix(1,2);

%VTI (the market) returns NaN, should be 1
if(isnan(b))
    b=1;
end