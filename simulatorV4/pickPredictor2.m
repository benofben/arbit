function window=pickPredictor2()

for(window=1:500)
    [prediction, truePositive, falsePositive, accuracy] = predictor2(window);
    a(window)=accuracy;
end

h=plot(a);
xlabel('Window');
ylabel('Accuracy');
saveas(h,'predictor2.jpg','jpg');

[y,window]=max(a);