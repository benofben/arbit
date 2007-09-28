clear all;
for(x=1:20)
    b_margin=x/10;
    [truePositive, falsePositive, accuracy] = predictor1(b_margin);
    a(x,:)=[b_margin, accuracy];
end
