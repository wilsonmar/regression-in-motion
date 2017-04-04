function [ sumsq ] = avgsq_residuals( xs, ys, preds )
%UNTITLED13 Summary of this function goes here
%   Detailed explanation goes here

sumsq = 0;
for i = 1:size(xs, 2)
    sumsq = sumsq + (ys(i)-preds(i))^2;
end
sumsq = sumsq / size(xs, 2);

end

