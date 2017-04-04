function draw_histogram(xs, ys, filename, nbuckets)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

if nargin < 4
    nbuckets = 6;
end

close all;
figure(1);

X = [ones(length(xs),1) xs'];
b = X \ ys';
ys1 = b(1) + b(2)*xs;
rs = ys - ys1;
histogram(rs);
title('Histogram of Residuals')
print(filename,'-dpng');
end
