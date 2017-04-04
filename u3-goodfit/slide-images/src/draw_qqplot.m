function draw_qqplot(xs, ys, filename)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

close all;
figure(1);

X = [ones(length(xs),1) xs'];
b = X \ ys';
ys1 = b(1) + b(2)*xs;
rs = ys - ys1;
qqplot(rs);
hold on;
%plot([-2, 2], [-2, 2], ':g');
title('QQ Plot of Residuals vs Normal Distribution')
ylabel('Quantiles of Residuals')
axis equal;
grid on;
print(filename,'-dpng');
end
