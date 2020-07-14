%root='C:\Users\Vicenç Salas\Desktop\CAP1\Entre_Labs';
%% Entre prova 1 i prova 2 no  hi ha cap diferencia de dia o escenari, 
%  només són dos instants diferents recollits amb l'osciloscopi
filename = 'Proves consum capitol 1';
sheet = 1;

dadesC1 = xlsread(filename,1);
dadesC2 = xlsread(filename,2);
time=dadesC1(:,1);
volt_C1=dadesC1(:,2);
volt_C2=dadesC2(:,2);
figure(); plot(time,volt_C1,time,volt_C2);
xlabel('Time(s)')
ylabel('Voltatge(V)')
title('Consum de la placa en prova entre laboratoris Prova1')
legend('Consum Lopy','Pin P12')

dadesC1 = xlsread(filename,3);
dadesC2 = xlsread(filename,4);
time=dadesC1(:,1);
volt_C1=dadesC1(:,2);
volt_C2=dadesC2(:,2);
figure(); plot(time,volt_C1,time,volt_C2);
xlabel('Time(s)')
ylabel('Voltatge(V)')
title('Consum de la placa en prova entre laboratoris Prova2')
legend('Consum Lopy','Pin P12')