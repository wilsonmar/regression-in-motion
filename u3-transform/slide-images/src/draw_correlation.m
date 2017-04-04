function draw_correlation(xs, ys, filename, axlimits)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

if nargin < 4
  axlimits = [0, 20, 0, 15];
end
close all;
figure(1);

xs1 = (xs - mean(xs)) / std(xs);
ys1 = (ys - mean(ys)) / std(ys);

ax = scatter(xs1, ys1, 'fill');
grid on;
axis(axlimits);
axis equal;

X = [ones(length(xs),1) xs1'];
b = X \ ys1';
xs2 = linspace(axlimits(1), axlimits(2));
ys2 = b(1) + b(2)*xs2;
hold on;
plot(xs2, ys2, '-r');
title('Linear Fit of Centered and Scaled Predictor and Response Variables')

print(filename,'-dpng');
end

