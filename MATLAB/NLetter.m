function [x,y] = NLetter(xi,yi,s)
    [x1,y1] = line2P(xi,yi,xi+2*s,yi);
    [x2,y2] = line2P(xi+2*s,yi,xi,yi-s);
    [x3,y3] = line2P(xi,yi-s,xi+2*s,yi-s);
    x = [x1;x2;x3];
    y = [y1;y2;y3];
end