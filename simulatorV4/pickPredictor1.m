function b_margin=pickPredictor1()

resolution=100;
for(x=1:resolution)
    b_margin=1+x/(resolution/2);
    [prediction, truePositive, falsePositive, accuracy] = predictor1(b_margin);
    a(x,:)=[b_margin, accuracy];
end

h=plot(a(:,1),a(:,2));
xlabel('Beta Margin');
ylabel('Accuracy');
saveas(h,'predictor1.jpg','jpg');

[y,i]=max(a(:,2));
b_margin=a(i,1);