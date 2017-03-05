rng(1066);

xs = 10:10:90;
ys = xs + 10 - 20*rand(1, 9);

ys1 = xs;
ys2 = .8*xs + 15;

error1 = avgsq_residuals(xs, ys, ys1);
error2 = avgsq_residuals(xs, ys, ys2);

close all;
figure(1);

axis tight manual;
axis([0, 10, 0, 20, 0, 100]);

scatter3([1, 0.8], [0, 15], [error1, error2], 'filled', 'red');

print('../error-graph-1','-dpng');


close all;
figure(1);

[ms, bs] = meshgrid(linspace(-5, 5, 40), linspace(-20, 20, 40));
es = zeros(size(ms));
for i = 1:size(ms,1)
    for j = 1:size(ms,2)
        preds = ms(i,j)*xs + bs(i,j);
        es(i,j) = avgsq_residuals(xs, ys, preds);
    end
end
mesh(ms, bs, es);

title('Error in Linear Regression Fit');
xlabel('Slope M');
ylabel('Intercept B');

print('../error-graph-real','-dpng');

close all;
figure(1);

[ms, bs] = meshgrid(linspace(-5, 5, 40), linspace(-5, 5, 40));
es = zeros(size(ms));
for i = 1:size(ms,1)
    for j = 1:size(ms,2)
        es(i,j) = ms(i,j)*ms(i,j) + bs(i,j)*bs(i,j);
    end
end
alpha(.5);
m = mesh(ms, bs, es);
%set(m, 'facecolor', 'none');

alpha(1);

hold on;

scatter3([ms(5,10)], [bs(5,10)], [es(5,10)], 100, 'filled', 'red');

title('Error in Linear Regression Fit');
xlabel('Slope M');
ylabel('Intercept B');

print('../gradient-descent-start','-dpng');

ixs = linspace(ms(5,10), 0, 100);
iys = linspace(bs(5,10), 0, 100);
hold on;
i = 15;
scatter3([ixs(i)], [iys(i)], [ixs(i)*ixs(i) + iys(i)*iys(i)], 100, 'filled', 'red');
print('../gradient-descent-next','-dpng');



vw = VideoWriter('../gradient-descent-animation.mp4', 'MPEG-4');
open(vw);

close all;
%figure('Position', [400, 100, 512, 512]);
fig = figure(1);
set(gca, 'nextplot', 'replacechildren');

ixs = linspace(ms(5,10), 0, 100);
iys = linspace(bs(5,10), 0, 100);

for i = 1:size(ixs,2)
    hold off;

    alpha(.5);
    m = mesh(ms, bs, es);
    alpha(1);

    hold on;

    scatter3([ixs(i)], [iys(i)], [ixs(i)*ixs(i) + iys(i)*iys(i)], 100, 'filled', 'red');

    title('Error in Linear Regression Fit');
    xlabel('Slope M');
    ylabel('Intercept B');

    frame = getframe(fig);
    writeVideo(vw, frame);
end

close(vw);




