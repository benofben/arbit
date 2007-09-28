function prediction = predictor1(symbolIndex)

% this is cheating right now.  Beta is being computed over everything in
% data/train

load b;
prediction=b(symbolIndex);