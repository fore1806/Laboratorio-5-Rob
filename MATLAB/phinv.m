function [q1,q2,q3,q4,q5]=phinv(x,y,z,q5p)
    %Triangulo constante
    h=106.5;%distancia diagonal entre q2 y q3
    c=sqrt(h^2-100^2); %cateto de la diagonal
    delta = atan2(c,100);

    q1=atan2(y,x);

    dmar0 = [x y z 1]'; %Posición del marcador
    d3 = 100*[cos(q1) sin(q1) 0 1/100]'; %Posición de la muñeca desde el marcador
    dw0 = dmar0-d3; %Posición de la muñeca desde la base

    %Altura relativa de la muñeca
    dz = dw0(3)-94;

    %Distancia de la muñeca al eje de la articulación2
    r2 = (dw0(1))^2+(dw0(2))^2+(dz)^2;
    r = sqrt(r2);

    %Teorema del coseno
    alpha = acos((100^2+r2-h^2)/(2*r*100));
    beta = acos((r2+h^2-100^2)/(2*r*h));
    gamma = acos((h^2+100^2-r2)/(2*h*100));

    %Ángulos auxiliares
    theta = atan2(dz,sqrt((dw0(1))^2+(dw0(2))^2));
    psi = pi-alpha;
    phi = pi-psi-theta;
    omega = pi-phi;
    kappa = omega-pi/2;

    %Posiciones angulares del manipulador
    q2= -(pi/2-theta-beta-delta-pi/18);
    q3= -(pi-gamma-(pi/2-delta));
    q4 = (pi/2-kappa);
    q5 = q5p;
end