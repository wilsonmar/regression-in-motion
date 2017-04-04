function draw_residuals(xs, ys, filename, axlimits)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

if nargin < 4
  axlimits = [0, 20, 0, 15];
end

close all;
figure(1);

grid on;
axis(axlimits);
axis equal;

X = [ones(length(xs),1) xs'];
b = X \ ys';
ys1 = b(1) + b(2)*xs;
rs = ys - ys1;
scatter(xs, rs, 'filled');
hold on;
plot([axlimits(1), axlimits(2)], [0, 0], '-r');
for i = 1:length(xs)
    plot([xs(i), xs(i)], [0, rs(i)], ':b');
end
title('Residuals for Best Linear Fit')
print(filename,'-dpng');
end
