function [x,y] = ILetter(xi,yi,s,N)
    [x1,y1] = line2P(xi,yi,xi+s,yi,N);
    [x2,y2] = line2P(xi+s,yi,xi+2*s,yi,N);
    x = [x1;x2];
    y = [y1;y2];
end