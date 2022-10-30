function [x,y] = circleDiscrete(xC,yC,r,n)
    theta = linspace(0,360,n);
    x = xC+r*cosd(theta);
    y = yC+r*sind(theta);
end