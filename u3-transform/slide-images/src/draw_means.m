function draw_means(xs, ys, filename, axlimits)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

if nargin < 4
  axlimits = [0, 20, 0, 15];
end
close all;
figure(1);

ax = scatter(xs, ys, 'fill');
grid on;
axis(axlimits);
axis equal;

hold on;

xmu = mean(xs);
ymu = mean(ys);
plot([axlimits(1), axlimits(2)], [ymu, ymu], '-.r')
plot([xmu, xmu], [axlimits(3), axlimits(4)], '-.r')
title('Mean Values of Predictor and Response Variables')

print(filename,'-dpng');
end

