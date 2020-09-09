%root='C:\Users\Vicenç Salas\Desktop\CAP1\Entre_Labs';
%% Entre prova 1 i prova 2 no  hi ha cap diferencia de dia o escenari, 
%  només són dos instants diferents recollits amb l'osciloscopi
%% Aqui es grafica el consum de la placa V(t)
filename = 'ConsumTomeu27_11';
sheet = 1;

dadesC1 = xlsread(filename,1);
dadesC2 = xlsread(filename,2);
time=dadesC1(:,1);
volt_C1=dadesC1(:,2);
volt_C2=dadesC2(:,2);
%%
figure1 = figure();
axes1 = axes('Parent', figure1);
%box(axes1,'on');
hold(axes1,'all');
plot(time,volt_C1,'Parent', axes1);
%%
axes2 = axes('Parent', figure1, 'YAxisLocation','right');
hold(axes2,'all');
plot(time,volt_C2, 'Parent', axes2);
xlabel('Time(s)')
ylabel('Voltatge(V)')
title('Consum de la placa en prova entre laboratoris Prova1')
legend('Consum Lopy','Pin P12')

%%
%dadesC1 = xlsread(filename,3);
%dadesC2 = xlsread(filename,4);
%time=dadesC1(:,1);
volt_C1=5-dadesC1(:,2);
volt_C2=dadesC2(:,2);
figure(); plot(time,volt_C1,time,volt_C2);
xlabel('Time(s)')
ylabel('Voltatge(V)')
title('Consum de la placa en prova entre laboratoris Prova2')
legend('Consum Lopy','Pin P12')

%% Aqui es grafica el comportament del canal snr, rssi
filename2 = 'Dades NodeRed capitol 1';
sheet = 2;

dades_entre_labs = xlsread(filename2,'Prova entre LABs');
[~, ~, raw, dates] = xlsread(filename2,'Prova entre LABs','Q2:Q463','',@convertSpreadsheetExcelDates);
dates = dates(:,1);
date_time = datetime([dates{:,1}].', 'ConvertFrom', 'Excel');
clearvars raw dates;

rssi=dades_entre_labs(2:463,11);
snr=dades_entre_labs(2:463,12);
figure(); plot(date_time,rssi);
xlabel('Time(dd/mm/yyyy hh:mm:ss)')
ylabel('Rssi')
title('Rssi prova entre laboratoris')

figure(); plot(date_time,snr);
xlabel('Time(dd/mm/yyyy hh:mm:ss)')
ylabel('SNR')
title('SNR prova entre laboratoris')

