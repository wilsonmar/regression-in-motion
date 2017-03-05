close all;

figure(1);

xs = [10; 90];
ys = [10; 90];
scatter(xs, ys, 'fill');
grid on;
axis([0, 100, 0, 100]);

print('../points-2','-dpng');

close all;

figure(1);

xs = [10; 60; 90];
ys = [10; 30; 90];
scatter(xs, ys, 'fill');
grid on;
axis([0, 100, 0, 100]);

print('../points-3','-dpng');

close all;

figure(1);

xs = [10; 60; 90];
ys = [10; 30; 90];
scatter(xs, ys, 'fill');
grid on;
axis([0, 100, 0, 100]);
hold on;
plot_line(10, 10, 90, 90);
plot_line(10, 20, 90, 80);
plot_line(20, 10, 90, 85);


print('../points-3-lines','-dpng');
