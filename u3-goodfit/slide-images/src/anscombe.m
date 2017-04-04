
rng(1067);

xs = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5];
ys = [ 8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68];
draw_regression(xs, ys, 'anscombe1')
draw_residuals(xs, ys, 'anscombe-residuals1')
draw_histogram(xs, ys, 'anscombe-histograms1')
draw_qqplot(xs, ys, 'anscombe-qqresiduals1')

xs = [10.0, 8.0, 13.0, 9.0, 11.0, 14.0, 6.0, 4.0, 12.0, 7.0, 5.0];
ys = [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74];
draw_regression(xs, ys, 'anscombe2')
draw_residuals(xs, ys, 'anscombe-residuals2')
draw_histogram(xs, ys, 'anscombe-histograms2')
draw_qqplot(xs, ys, 'anscombe-qqresiduals2')

xs = [10.0, 8.0, 13.0, 9.0, 11.0, 14.0, 6.0, 4.0, 12.0, 7.0, 5.0];
ys = [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73];
draw_regression(xs, ys, 'anscombe3')
draw_residuals(xs, ys, 'anscombe-residuals3')
draw_histogram(xs, ys, 'anscombe-histograms3')
draw_qqplot(xs, ys, 'anscombe-qqresiduals3')

xs = [ 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 19.0, 8.0, 8.0, 8.0];
ys = [ 6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89];
draw_regression(xs, ys, 'anscombe4')
draw_residuals(xs, ys, 'anscombe-residuals4')
draw_histogram(xs, ys, 'anscombe-histograms4')
draw_qqplot(xs, ys, 'anscombe-qqresiduals4')


