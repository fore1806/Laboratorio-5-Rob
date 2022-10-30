function [x,y] = FLetter(xi,yi,s)
    [x1,y1] = line2P(xi,yi,xi+s,yi);
    [x2,y2] = line2P(xi+s,yi,xi+s,yi-s);
    [x3,y3] = line2P(xi+s,yi-s,xi+s,yi);
    [x4,y4] = line2P(xi+s,yi,xi+2*s,yi);
    [x5,y5] = line2P(xi+2*s,yi,xi+2*s,yi-s);
    x = [x1;x2;x3;x4;x5];
    y = [y1;y2;y3;y4;y5];
end