function [x,y] = Parallel(xi,yi,s,L)
    [x1,y1] = line2P(xi,yi,xi,yi-L);
    [x2,y2] = line2P(xi+s,yi,xi+s,yi-L);
    [x3,y3] = line2P(xi+2*s,yi,xi+2*s,yi-L);
    x = [x1;x2;x3];
    y = [y1;y2;y3];
end