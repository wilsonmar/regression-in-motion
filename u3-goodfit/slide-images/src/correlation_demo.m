rng(1067);

xs = linspace(1, 10);
ys = 2 + .3 * xs;
r = corrcoef(xs,ys);
r(1, 2)
draw_regression(xs, ys, 'correlation-1', [0, 10, 0, 10])

xs = linspace(1, 10);
ys = 5 - .3 * xs;
r = corrcoef(xs,ys);
r(1, 2)
draw_regression(xs, ys, 'correlation-minus-1', [0, 10, 0, 10])

xs = linspace(1, 10);
ys = .7 * xs + randn(size(xs));
r = corrcoef(xs,ys);
r(1, 2)
draw_regression(xs, ys, 'correlation-,9', [0, 10, 0, 10])

xs = linspace(1, 10);
ys = 7 - .7 * xs + randn(size(xs));
r = corrcoef(xs,ys);
r(1, 2)
draw_regression(xs, ys, 'correlation-minus,9', [0, 10, 0, 10])

xs = linspace(1, 10);
ys = .7 * xs + 4 * randn(size(xs));
r = corrcoef(xs,ys);
r(1, 2)
draw_regression(xs, ys, 'correlation-,4', [0, 10, 0, 10])

xs = linspace(1, 10);
ys = 7 - .7 * xs + 4 * randn(size(xs));
r = corrcoef(xs,ys);
r(1, 2)
draw_regression(xs, ys, 'correlation-minus,5', [0, 10, 0, 10])

xs = linspace(1, 10);
ys = 5 + 4 * randn(size(xs));
r = corrcoef(xs,ys);
r(1, 2)
draw_regression(xs, ys, 'correlation-0,1', [0, 10, 0, 10])

xs = linspace(1, 10);
ys = 5 + 5*sin(xs);
r = corrcoef(xs,ys);
r(1, 2)
draw_regression(xs, ys, 'correlation-sine', [0, 10, 0, 10])

xs = linspace(1, 10);
ys = xs.^2 / 10;
r = corrcoef(xs,ys);
r(1, 2)
draw_regression(xs, ys, 'correlation-xsq', [0, 10, 0, 10])

xs = [ xs, linspace(10, 20) ];
ys = xs.^2 / 10;
draw_regression(xs, ys, 'correlation-extrapolate', [0, 20, 0, 40], 100)

xs = linspace(1, 10);
ys = .1 * xs;
ys(100) = 20;
r = corrcoef(xs,ys);
r(1, 2)
draw_regression(xs, ys, 'correlation-outlier', [0, 10, 0, 20])

xs = linspace(1, 10);
ys = 5 + 2.5*randn(size(xs));
r = corrcoef(xs,ys);
r(1, 2)
draw_regression(xs, ys, 'correlation-interpolate-1', [0, 10, 0, 20])

xs1 = 95;
ys1 = 50 + 2.5*randn(size(xs1));
xs = [xs, xs1];
ys = [ys, ys1];
r = corrcoef(xs,ys);
display('The answer is ')
r(1, 2)
draw_regression(xs, ys, 'correlation-interpolate-2', [0, 10,  0, 20])
draw_regression(xs, ys, 'correlation-interpolate-3', [0, 100, 0, 80])

xs = 1:5;
ys = xs.^3/10 + 1;
draw_regression(xs, ys, 'correlation-transformation-1', [0, 6,  0, 15])

xs = 1:5;
ys = xs.^3/10 + 1;
xs = xs.^2;
draw_regression(xs, ys, 'correlation-transformation-2', [0, 25,  0, 15])

xs = 1:5;
ys = xs.^3/10 + 1;
xs = xs.^3;
draw_regression(xs, ys, 'correlation-transformation-3', [0, 125,  0, 15])

xs = 1:5;
ys = xs.^3/10 + 1;
xs3 = xs.^3;
close all;
figure(1);
scatter(xs, ys, 'fill');
hold on;
grid on;
axis([0, 6,  0, 15]);
axis equal;

X = [ones(length(xs3),1) xs3'];
b = X \ ys';
xs1 = linspace(1, 5);
xs1 = xs1;
ys1 = b(1) + b(2)*xs1.^3;
hold on;
plot(xs1, ys1, '-r');
title('Best Linear Fit')

print('correlation-transformation-4','-dpng');
