% Solve a Pattern Recognition Problem with a Neural Network
% Script generated by NPRTOOL
% Created Thu Apr 21 16:40:42 EST 2016
%
% This script assumes these variables are defined:
%
%   in - input data.
%   out - target data.
function [net,outputs, performance, percentCorrect, trainFcn, hiddenLayerSize, tr] = feedforward_net(in, out, trainFcn, hiddenLayerSize)
inputs = in';
targets = out';

% Create a Pattern Recognition Network
% hiddenLayerSize = 250
% trainFcn = 'trainscg';
% trainFcn = 'trainlm'
net = feedforwardnet(hiddenLayerSize, trainFcn);


% Setup Division of Data for Training, Validation, Testing
net.divideParam.trainRatio = 75/100;
net.divideParam.valRatio = 5/100;
net.divideParam.testRatio = 20/100;

%prevent gui stuff
net.trainParam.showWindow = false;
net.trainParam.showCommandLine = false;

% Train the Network
[net,tr] = train(net,inputs,targets);

% Test the Network
outputs = net(inputs);
errors = gsubtract(targets,outputs);
performance = perform(net,targets,outputs);

% View the Network
view(net);

% Plots
% Uncomment these lines to enable various plots.
% figure, plotperform(tr);
% figure, plottrainstate(tr);
% figure, plotconfusion(targets,outputs);
% figure, plotroc(targets,outputs);
% figure, ploterrhist(errors);


percentCorrect = getMissRate(out', outputs);
end