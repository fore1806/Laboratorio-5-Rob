function [x,y] = ILetter(xi,yi,s)
    [x,y] = line2P(xi,yi,xi+2*s,yi);
end