
rng(1067);

data = csvread('experiment-springs.csv', 2, 0);
xs = data(:,2)';
ys = data(:,1)';
draw_regression(xs, ys, 'springs', [-1, 11, -1, 11])
draw_means(xs, ys, 'springs-means', [-1, 11, -1, 11])
draw_centered(xs, ys, 'springs-centered', [-6, 6, -6, 6])
draw_centered_scaled(xs, ys, 'springs-centered-scaled', [-2, 2, -2, 2])
draw_correlation(xs, ys, 'springs-correlation', [-2, 2, -2, 2])
draw_residuals(xs, ys, 'springs-residuals1', [-1, 11, -1, 11])
draw_histogram(xs, ys, 'springs-histograms1', 10)
draw_qqplot(xs, ys, 'springs-qqresiduals1')

data = csvread('experiment-refraction.csv', 2, 0);
xs = data(:,2)';
ys = data(:,1)';
r = corrcoef(xs,ys);
r(1, 2)
draw_regression(xs, ys, 'refraction', [-0.1, 2, -0.1, 1.2])
draw_means(xs, ys, 'refraction-means',[-0.1, 2, -0.1, 1.2])
draw_centered(xs, ys, 'refraction-centered',[-1, 1, -0.6, 0.6])
draw_centered_scaled(xs, ys, 'refraction-centered-scaled',[-2, 2, -2, 2])
draw_correlation(xs, ys, 'refraction-correlation',[-2, 2, -2, 2])
draw_residuals(xs, ys, 'refraction-residuals',[-0.1, 2, -0.1, 2])
draw_histogram(xs, ys, 'refraction-histograms', 10)
draw_qqplot(xs, ys, 'refraction-qqresiduals')

