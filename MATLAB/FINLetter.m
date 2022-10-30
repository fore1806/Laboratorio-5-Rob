function [x,y] = FINLetter(xi,yi,s)
    [x1,y1] = FLetter(xi,yi,s);
    [x2,y2] = ILetter(xi,yi-s-10,s);
    [x3,y3] = NLetter(xi,yi-s-20,s);
    x = [x1;x2;x3];
    y = [y1;y2;y3];
end