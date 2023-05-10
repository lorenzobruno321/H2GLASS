clear
close all
clc

set(0,'defaultaxesfontsize',14)
set(0,'defaultlinelinewidth',1)

%% POWER LOAD APPROXIMATION - constant profile
pow_avg=42.2;                              %[MW/week]
pow_hour=pow_avg*1000/7/24;                %[kW/hour]
time=(1:365*24)';
pow_output=pow_avg*ones(size(time));

figure(1)
plot(time,pow_output,'b-')               %time*min_pow;
hold on
box on
grid on
xlabel('time [h]')
ylabel('thermal load [MW]')
title('Approximation of thermal load in a steel furnace in one year')
set(gcf,'color','w')

[AA list_pv list_grid]=xlsread('Results.xlsx');

figure(2)
plot(AA(:,1),AA(:,2),'r-')               
hold on
plot(AA(:,1),AA(:,3),'b-')
box on
grid on
xlabel('time [h]')
% ylabel('thermal load [MW]')
legend('PV power [kW]','GRID power [kW]')
title('Power supply to the electrolyser to produce hydrogen')
set(gcf,'color','w')

figure(3)
plot(AA(:,1),AA(:,2),'r-')               
hold on
box on
grid on
xlabel('time [h]')
ylabel('PV power supply [kW]')
title('Power supply from the PV generation')
set(gcf,'color','w')

figure(4)
plot(AA(:,1),AA(:,3),'b-')               
hold on
box on
grid on
xlabel('time [h]')
ylabel('GRID power supply [kW]')
title('Power supply from the GRID')
set(gcf,'color','w')