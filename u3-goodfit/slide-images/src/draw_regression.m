function draw_regression(xs, ys, filename, axlimits, nlimit)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

if nargin < 4
  axlimits = [0, 20, 0, 15];
end
if nargin < 5
    nlimit = length(xs);
end
close all;
figure(1);

xs0 = xs(1:nlimit);
ys0 = ys(1:nlimit);
scatter(xs0, ys0, 'fill');
hold on;
if nlimit < length(xs)
    scatter(xs(nlimit+1:length(xs)), ys(nlimit+1:length(xs)), '.b')
end
grid on;
axis(axlimits);
axis equal;

X = [ones(length(xs0),1) xs0'];
b = X \ ys0';
xs1 = linspace(axlimits(1), axlimits(2));
ys1 = b(1) + b(2)*xs1;
hold on;
plot(xs1, ys1, '-r');
title('Best Linear Fit')

print(filename,'-dpng');

end
