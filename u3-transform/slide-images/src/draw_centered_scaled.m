function draw_centered_scaled(xs, ys, filename, axlimits)
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

hold on;
plot([axlimits(1), axlimits(2)], [0, 0], '-.r')
plot([0, 0], [axlimits(3), axlimits(4)], '-.r')

title('Centered and Scaled Predictor and Response Variables')

print(filename,'-dpng');
end

