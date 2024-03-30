if flag==0; Hcmg=Hcmg;else;Hcmg=HcmgMP;end;
Hxcmg=[];Hycmg=[];Hzcmg=[];CondA=[]; CondA_MP=[];t=[]; SingPt=[];DetA=[];
for i=1:max(size(A));  t=[t i*DeltaT];  H=Hcmg(:,:,i); Hx=H(1,:);  Hy=H(2,:);  Hz=H(3,:);
detA=det(A(:,1:3,i));Hxcmg=[Hxcmg Hx];  Hycmg=[Hycmg Hy];  Hzcmg=[Hzcmg Hz];
CONDA=cond(A(:,:,i));  CONDA_MP=cond(A_MP(:,:,i));  
DetA=[DetA detA]; CondA=[CondA CONDA];CondA_MP=[CondA_MP CONDA_MP];end;  
Hmag=sqrt(Hxcmg.^2+Hycmg.^2+Hzcmg.^2);x=(max(t)-DeltaT);

if flag==0; MaxInvCond=min(1./CondA(10*Rate+1:end));DELTA=delta;DELTAdot=deltadot;
else; MaxInvCond=min(1./CondA_MP(10*Rate+1:end));DELTA=delta_MP;DELTAdot=deltadot_MP;Hcmg=HcmgMP;end;
ERROR=trajectory*180/pi-Euler;

%openfig('90_Degree_Singularity_Hypersurface');hold on;plot3(Hcmg(1,:),Hcmg(2,:),Hcmg(3,:), 'LineWidth',3);hold off;

figure(2);
subplot(2,1,1);plot(t,Hmag,'LineWidth',2);   ylabel('|H_c_m_g|','Fontsize',12);grid;axis([0,x,0,3]);
subplot(2,1,2);plot(t,DetA,'linewidth',2);grid;xlabel('t(sec)','fontsize',12,'fontname','times');ylabel('det[A]','fontsize',12,'fontname','times');axis([0,x,-1,1]);


DELTA1=DELTA(1,:);DELTA2=DELTA(2,:);DELTA3=DELTA(3,:);DELTA4=DELTA(4,:);
DELTAdot1=DELTAdot(1,:);DELTAdot2=DELTAdot(2,:);DELTAdot3=DELTAdot(3,:);DELTAdot4=DELTAdot(4,:);

figure(3);subplot(3,1,1);plot(t,DELTA1,'LineWidth',2); ylabel('\theta_1(deg)','Fontsize',12);grid;axis([0,x,min(DELTA1),max(DELTA1)]);
subplot(3,1,2);plot(t,DELTA2,'LineWidth',2); ylabel('\theta_2(deg)','Fontsize',12);grid;axis([0,x,min(DELTA2),max(DELTA2)])
subplot(3,1,3);plot(t,DELTA3,'LineWidth',2); ylabel('\theta_3(deg)','Fontsize',12);grid;axis([0,x,min(DELTA3),max(DELTA3)]);xlabel('t(sec)','Fontsize',12);

figure(4);subplot(3,1,1);plot(t,DELTAdot1,'LineWidth',2);   ylabel('\theta_d_o_t_1(deg/s)','Fontsize',12);grid;axis([0,x,-pi*1.1,pi*1.1])
subplot(3,1,2);plot(t,DELTAdot2,'LineWidth',2);   ylabel('\theta_d_o_t_2(deg/s)','Fontsize',12);grid;axis([0,x,-pi*1.1,pi*1.1])
subplot(3,1,3);plot(t,DELTAdot3,'LineWidth',2);   ylabel('\theta_d_o_t_3(deg/s)','Fontsize',12);grid;axis([0,x,-pi*1.1,pi*1.1]);xlabel('t(sec)','Fontsize',12);

figure(5); 
subplot(3,1,1);plot(t,Hxcmg,'linewidth',2);axis([0,x,-3.25,3.25]);grid;ylabel('h_x/|h|','fontsize',14);title('Normalized Momentum','fontsize',14);
subplot(3,1,2);plot(t,Hycmg,'linewidth',2);axis([0,x,-3.25,3.25]);grid;ylabel('h_y/|h|','fontsize',14);
subplot(3,1,3);plot(t,Hzcmg,'linewidth',2);axis([0,x,-3.25,3.25]);grid;ylabel('h_z/|h|','fontsize',14);xlabel('t(sec)','fontsize',14);

figure(6); EulerX=Euler(:,1);EulerY=Euler(:,2);EulerZ=Euler(:,3);
subplot(3,1,1);plot(t,EulerX,'linewidth',2);  axis([0,x,-5,5]);          %axis([0,x,min(EulerX)*1.1,max(EulerX)*1.1]);
                       grid;ylabel('\phi(deg)','fontsize',16);title('Euler Angles','fontsize',14);
subplot(3,1,2);plot(t,EulerY,'linewidth',2);axis([0,x,-5,1.1*max(EulerY)]);  %axis([0,x,min(EulerY)*1.1,max(EulerY)*1.1]);
                        grid;ylabel('\theta(deg)','fontsize',16);
subplot(3,1,3);plot(t,EulerZ,'linewidth',2);axis([0,x,-5,1.1*max(EulerZ)]);  %axis([0,x,min(EulerZ)*1.1,max(EulerZ)*1.1]);
                        grid;ylabel('\psi(deg)','fontsize',16);xlabel('t(sec)','fontsize',14);
EX=ERROR(:,1);EY=ERROR(:,2);EZ=ERROR(:,3);
MeanXerror=mean(EX); Xmean=num2str(MeanXerror); xmean=['\mu_x=', Xmean];
STDx=std(EX);Xsigma=num2str(STDx);SigmaX=['\sigma_x=' Xsigma]; 
MeanYerror=mean(EY); Ymean=num2str(MeanYerror); ymean=['\mu_y=', Ymean];
STDy=std(EY); Ysigma=num2str(STDy);SigmaY=['\sigma_y=' Ysigma]; 
MeanZerror=mean(EZ); Zmean=num2str(MeanZerror); zmean=['\mu_z=', Zmean];
STDz=std(EZ);Zsigma=num2str(STDz);SigmaZ=['\sigma_z=' Zsigma]; 
MeanError=[MeanXerror MeanYerror MeanZerror];  StdDev=[STDx STDy STDz];

figure(7); 
subplot(3,1,1);plot(t,EX,'linewidth',2);axis([0,x,-5,5]);  % axis([0,x,min(EX)*1.1,max(EX)*1.1]); 
  grid;ylabel('\phi(deg)','fontsize',16);title('Tracking Error','fontsize',14);
  text(x*2/3,max(EX)*2/3,xmean,'fontsize',12,'fontname','times');  text(x*2/3,max(EX)*1/3,SigmaX,'fontsize',12,'fontname','times');
subplot(3,1,2);plot(t,EY,'linewidth',2);axis([0,x,-5,5]);  %axis([0,x,min(EY)*1.1,max(EY)*1.1]);
  grid;ylabel('\theta(deg)','fontsize',16);
  text(x*2/3,min(EY)*2/3,ymean,'fontsize',12,'fontname','times');  text(x*2/3,min(EY)*1/3,SigmaY,'fontsize',12,'fontname','times');
subplot(3,1,3);plot(t,EZ,'linewidth',2);axis([0,x,-5,5]);  %axis([0,x,min(EZ)*1.1,max(EZ)*1.1]);
  grid;ylabel('\psi(deg)','fontsize',16);xlabel('t(sec)','fontsize',14);
  text(x*2/3,max(EZ)*2/3,zmean,'fontsize',12,'fontname','times');  text(x*2/3,max(EZ)*1/3,SigmaZ,'fontsize',12,'fontname','times');
EX(end,:)
EY(end,:)
EZ(end,:)

figure(8);
subplot(3,1,1);plot(t,ufb(:,1),'linewidth',2);grid; axis([0, max(t),min(ufb(:,1)),max(ufb(:,1))]);  
ylabel('u_f_b_\phi','fontname','times','fontsize',20);
subplot(3,1,2);plot(t,ufb(:,2),'linewidth',2);grid; axis([0, max(t),min(ufb(:,2)),max(ufb(:,2))]);  
ylabel('u_f_b_\theta','fontname','times','fontsize',20);
subplot(3,1,3);plot(t,ufb(:,3),'linewidth',2);grid; axis([0, max(t),min(ufb(:,3)),max(ufb(:,3))]);  
ylabel('u_f_b_\psi','fontname','times','fontsize',20);xlabel('time (sec)','fontname','times','fontsize',20);
  
figure(9);
subplot(3,1,1);plot(t,uff(:,1),'linewidth',2);grid; %axis([0, max(t),min(uff(:,1)),max(uff(:,1))]);  
ylabel('u_f_f_\phi','fontname','times','fontsize',20);
subplot(3,1,2);plot(t,uff(:,2),'linewidth',2);grid; %axis([0, max(t),min(uff(:,2)),max(uff(:,2))]);  
ylabel('u_f_f_\theta','fontname','times','fontsize',20);
subplot(3,1,3);plot(t,uff(:,3),'linewidth',2);grid; %axis([0, max(t),min(uff(:,3)),max(uff(:,3))]);  
ylabel('u_f_f_\psi','fontname','times','fontsize',20);xlabel('time (sec)','fontname','times','fontsize',20);
