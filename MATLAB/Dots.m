function [x,y] = Dots(xi,yi,s,N)
    x = zeros(1,N);
    y = zeros(1,N);
    for i=1:N
        x(i) = xi+s*(i-1);
        y(i) = yi+s*(i-1);
    end
end