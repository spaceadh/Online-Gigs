clear all;  close all;  clc;
MaxError=[];  Kd=[];  K=[];MeanX=[];MeanY=[];MeanZ=[];ratio=[];

for j=0.1:0.01:1
    Ratio=j
    sim('Working_TASS2_Fossen_Smoothed.mdl');
    ErrorX=ERROR(:,1);ErrorY=ERROR(:,2);ErrorZ=ERROR(:,3);
    MeanX=[MeanX mean(abs(ErrorX))];    MeanY=[MeanY mean(abs(ErrorY))];
    MeanZ=[MeanZ mean(abs(ErrorZ))];    ratio=[ratio Ratio];
end    

subplot(3,1,1);plot(ratio,MeanX);grid;ylabel('\mu_X (deg)','fontname','times','fontsize',20)
subplot(3,1,2);plot(ratio,MeanY);grid;ylabel('\mu_Y (deg)','fontname','times','fontsize',20)
subplot(3,1,3);plot(ratio,MeanZ);grid;ylabel('\mu_Z (deg)','fontname','times','fontsize',20)
xlabel('Ratio of current \omega_d_o_t','fontname','times','fontsize',20)