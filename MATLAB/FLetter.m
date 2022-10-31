function [x,y] = FLetter(xi,yi,s,N)
    A=5;
    [x1,y1] = line2P(xi,yi,xi+s,yi,N);
    [x2,y2] = line2P(xi+s,yi,xi+s,yi-s,N);
    [x3,y3] = line2P(xi+s,yi-s,xi+s,yi,N);
    [x4,y4] = line2P(xi+s,yi+A,xi+2*s,yi+A,N);
    [x5,y5] = line2P(xi+2*s,yi+A,xi+2*s,yi-s-A,N);
    x = [x1;x2;x3;x4;x5];
    y = [y1;y2;y3;y4;y5];
end