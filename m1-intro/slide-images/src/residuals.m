rng(1066);

xs = 10:10:90;
ys = xs + 5 + 5*randn(1, 9);


close all;
figure(1);

scatter(xs, ys, 'fill');
grid on;
axis([0, 100, 0, 100]);

print('../points-10','-dpng');

close all;
figure(1);

scatter(xs, ys, 'fill');
hold on;
ys1 = xs + 5;
plot(xs, ys1, '-r');
grid on;
axis([0, 100, 0, 100]);

print('../points-10-1','-dpng');

close all;
figure(1);

scatter(xs, ys, 'fill');
hold on;
ys2 = .8*xs + 15;
plot(xs, ys1, '-r');
plot(xs, ys2, '-b');
grid on;
axis([0, 100, 0, 100]);

print('../points-10-2','-dpng');

close all;
figure(1);

scatter(xs, ys, 'fill');
hold on;
plot(xs, ys1, '-r');
sumsq = 0;
for i = 1:size(xs, 2)
    plot([xs(i), xs(i)], [ys(i), ys1(i)], '-r');
    text(xs(i)-5, (ys(i)+ys1(i))/2, sprintf('%.1f', ys(i)-ys1(i)),'Color','red');
    sumsq = sumsq + (ys(i)-ys1(i))^2;
end
sumsq = sumsq/size(xs,2);
grid on;
axis([0, 100, 0, 100]);

print('../points-10-res-1','-dpng');

text(50, 15, sprintf('Average of square of residuals = %.2f', sumsq),'Color','red');
print('../points-10-res-1b','-dpng');


close all;
figure(1);

scatter(xs, ys, 'fill');
hold on;
plot(xs, ys2, '-b');
sumsq = 0;
for i = 1:size(xs, 2)
    plot([xs(i), xs(i)], [ys(i), ys2(i)], '-b');
    text(xs(i)-5, (ys(i)+ys2(i))/2, sprintf('%.1f', ys(i)-ys2(i)),'Color','blue');
	sumsq = sumsq + (ys(i)-ys2(i))^2;
end
sumsq = sumsq/size(xs,2);
grid on;
axis([0, 100, 0, 100]);

print('../points-10-res-2','-dpng');

text(50, 15, sprintf('Average of square of residuals = %.2f', sumsq),'Color','blue');
print('../points-10-res-2b','-dpng');


vw = VideoWriter('../points-10-res-shift.mp4', 'MPEG-4');
open(vw);

close all;
%figure('Position', [400, 100, 512, 512]);
fig = figure(1);
set(gca, 'nextplot', 'replacechildren');

for dm = linspace(0, 1, 60)
    hold off;
    dy = -dm*(xs - 50); 
    scatter(xs, ys+dy, 'fill');
    hold on;
    plot(xs, ys1+dy, '-r');
    for i = 1:size(xs, 2)
        plot([xs(i), xs(i)], [ys(i), ys1(i)]+dy(i), '-r');
        text(xs(i)-5, dy(i)+(ys(i)+ys1(i))/2, sprintf('%.1f', ys(i)-ys1(i)),'Color','red');
    end
    grid on;
    axis([0, 100, 0, 100]);
    frame = getframe(fig);
    writeVideo(vw, frame);
end

close(vw);


