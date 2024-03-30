close all;clear all;clc;
% Enter [J] components as symbolic variables, then assemble [J]
syms Jxx; syms Jxy; syms Jxz;  syms Jyx; syms Jyy; syms Jyz;  syms Jzx; syms Jzy; syms Jzz;
J=[Jxx,  Jxy,  Jxz;  Jyx,  Jyy,  Jyz;   Jzx,  Jzy,  Jzz];
J=[Jxx,  Jxy,  Jxz;  Jxy,  Jyy,  Jyz;   Jxz,  Jyz,  Jzz]; % Assume symmetric [J]
% Enter [JhatStar] components as symbolic variables, then assemble [JhatStar]
syms JhatStarxx; syms JhatStarxy; syms JhatStarxz;  syms JhatStaryx; syms JhatStaryy; syms JhatStaryz;  syms JhatStarzx; syms JhatStarzy; syms JhatStarzz;
JhatStar=[JhatStarxx,  JhatStarxy,  JhatStarxz;  JhatStaryx,  JhatStaryy,  JhatStaryz;   JhatStarzx,  JhatStarzy,  JhatStarzz];
% Enter [ChatStar] components as symbolic variables, then assemble [ChatStar]
syms ChatStarxx; syms ChatStarxy; syms ChatStarxz;  syms ChatStaryx; syms ChatStaryy; syms ChatStaryz;  syms ChatStarzx; syms ChatStarzy; syms ChatStarzz;
ChatStar=[ChatStarxx,  ChatStarxy,  ChatStarxz;  ChatStaryx,  ChatStaryy,  ChatStaryz;   ChatStarzx,  ChatStarzy,  ChatStarzz];

% Enter {x} & {xdot} components as symbolic variables, then assemble {x} & {xdot}
syms phi;  syms theta;  syms psi;  x=[phi; theta; psi];
syms phidot;  syms thetadot;  syms psidot;  xdot=[phidot; thetadot; psidot];
% Enter {xD},{xDdot} & {xDddot} components as symbolic variables, then assemble {xD},{xDdot} & {xDddot}
syms phiD;  syms thetaD;  syms psiD;  xD=[phiD; thetaD; psiD];
syms phiDdot;  syms thetaDdot;  syms psiDdot;  xDdot=[phiDdot; thetaDdot; psiDdot];
syms phiDddot;  syms thetaDddot;  syms psiDddot;  xDddot=[phiDddot; thetaDddot; psiDddot];
% Enter Kd & lambda as symbolic variable and calculate xRdot & xRddot, then e
syms lambda; syms Kd;    xtilda=x-xD;   xtildadot=xdot-xDdot;
xRdot=xDdot-lambda*xtilda;  xRddot=xDddot-lambda*xtildadot;  e=xtildadot+lambda*xtilda;

% Enter [H] components as symbolic variables and assemble [H]
syms Hx; syms Hy; syms Hz; H=[0, -Hz, Hy; Hz, 0, -Hx; -Hy Hx 0];
% Assemble [S]
S=[1,                         0,                                                         -sin(theta);  
     0, cos(phi)/(sin(theta)*sin(phi)+cos(phi)^2),   sin(theta)*cos(theta)/(sin(theta)*sin(phi)+cos(phi)^2);
     0, -sin(phi)/(sin(theta)*sin(phi)+cos(phi)^2),   cos(theta)*cos(phi)/(sin(theta)*sin(phi)+cos(phi)^2)  ];
% Assemble [Sdot]
Sdot=[0, cos(phi)*phidot+sin(phi)*sec(theta)^2*thetadot,                                -sin(phi)*phidot*tan(theta)+cos(phi)*sec(theta)^2;  
          0,                 -sin(phi)*phidot,                                                                                       -cos(theta)*thetadot;
          0, (cos(theta)*cos(phi)*phidot+sin(phi)*sin(theta)*thetadot)/cos(theta)^2,  (-cos(theta)*sin(phi)*phidot+cos(phi)*sin(theta)*thetadot)/(cos(theta)^2)];
% Calculate Jstar and Cstar
Jstar=(S^-1)'*J*S^-1;Cstar=-(S^-1)'*J*S^-1*Sdot*S^-1-(S^-1)'*H*S^-1;
% Define JtildaStar and CtildaStar
JtildaStar=JhatStar-Jstar;   CtildaStar=ChatStar-Cstar;
% Multiply out JtildaStar*xRddot+CtildaStar*xRdot-Kd*e
LinearForm=JtildaStar*xRddot+CtildaStar*xRdot-Kd*e;
%xlswrite('LINEARFORM.xls',LinearForm);

