clear all;  close all;  clc;
MaxError=[];  Kd=[];  K=[];MeanX=[];MeanY=[];MeanZ=[];eta=[];
% yaw=20 & ETA=3
% yaw=30 & ETA=7  !!!
for j=1:10
    ETA=j-1
    yaw=45;    sim('Working_TASS2_Agrawal.mdl');
    ErrorX=ERROR(:,1);ErrorY=ERROR(:,2);ErrorZ=ERROR(:,3);
    MeanX=[MeanX mean(abs(ErrorX))];    MeanY=[MeanY mean(abs(ErrorY))];
    MeanZ=[MeanZ mean(abs(ErrorZ))];    eta=[eta ETA];
end    

subplot(3,1,1);plot(eta,MeanX);grid;ylabel('\mu_X (deg)','fontname','times','fontsize',20)
subplot(3,1,2);plot(eta,MeanY);grid;ylabel('\mu_Y (deg)','fontname','times','fontsize',20)
subplot(3,1,3);plot(eta,MeanZ);grid;ylabel('\mu_Z (deg)','fontname','times','fontsize',20)
xlabel('Adaption Gain, 10^o Maneuver','fontname','times','fontsize',20)