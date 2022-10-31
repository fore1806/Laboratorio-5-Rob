function [x,y] = Parallel(xi,yi,s,L,N)
    [x1,y1] = line2P(xi,yi,xi,yi-L,N);
    [x2,y2] = line2P(xi+s,yi,xi+s,yi-L,N);
    [x3,y3] = line2P(xi+2*s,yi,xi+2*s,yi-L,N);
    x = [x1;x2;x3];
    y = [y1;y2;y3];
end