clear all;  close all;  clc;
MaxError=[];  Kd=[];  K=[];MaxErr=[];eta=[];

for j=1:10000:2000001
    ETA=j
    sim('Working_TASS2_Agrawal.mdl');
    ErrorX=ERROR(:,1);ErrorY=ERROR(:,2);ErrorZ=ERROR(:,3);
    MaxError=[max(abs(ErrorX)) max(abs(ErrorY)) max(abs(ErrorZ))];
    MaxErr=[MaxErr max(MaxError)]; eta=[eta ETA];
end    
        
plot(eta,MaxErr);grid;
xlabel('Adaption Gain, 10^o Maneuver','fontname','times','fontsize',20)
ylabel('Max Tracking Error (deg)','fontname','times','fontsize',20)