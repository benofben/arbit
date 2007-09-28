for(window=1:500)
    [pGoodDay, truePositive, falsePositive, accuracy] = predictor2(window);
    a(window)=accuracy;
end
