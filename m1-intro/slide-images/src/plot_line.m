function [ output_args ] = plot_line( x1, y1, x2, y2, LineSpec )
%UNTITLED10 Summary of this function goes here
%   Detailed explanation goes here

xs = x1:x2;
ys = y2 - (y2-y1)/(x2-x1) * (x2 - xs);
if nargin<=4
    plot(xs, ys);
else
    plot(xs, ys, LineSpec);
end

end

