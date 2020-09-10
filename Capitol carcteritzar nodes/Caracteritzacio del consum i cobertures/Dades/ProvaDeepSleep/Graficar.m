%% Prova interior del nostre lab 5m
filename = 'PROVA4';%'DEEPSL01';
sheet = 1;

dades = xlsread(filename,sheet);
time=dades(:,1)/100000;
volt=5-(dades(:,2)/100000);

figure(); plot(time,volt);
xlabel('Temps(s)')
ylabel('Corrent(A)')
title('Consum del node a la prova 5m')% 4')
%%
filename ='DEEPSL01';
sheet = 1;

dades = xlsread(filename,sheet);
time=dades(:,1);
volt=dades(:,2);

figure(); plot(time,volt);
xlabel('Temps(s)')
ylabel('Corrent(A)')
title('Consum del node a la prova 5m - DeepSleep')% 4')

ids_deepsleep=find((volt<4.8)&(volt> 4.7805))
figure(); plot(time(ids_deepsleep),volt(ids_deepsleep));
xlabel('Time(s)')
ylabel('Voltatge(V)')
title('Detall del consum en mode Lopy to Lopy')
I_mean=mean(volt(ids_deepsleep))
I_comLora=(5-I_mean)/1

figure(); plot(time(ids_deepsleep),(5-volt(ids_deepsleep))*1000);
xlabel('Time(s)')
ylabel('Voltatge(mV)')
title('Detall del consum en mode deepsleep')

consum_deep=5-volt(ids_deepsleep);
mean(consum_deep)
std(consum_deep)

figure(); plot(time(ids_deepsleep),(5-volt(ids_deepsleep))*1000,time(ids_deepsleep),mean(consum_deep));
xlabel('Time(s)')
ylabel('Voltatge(mV)')
title('Detall del consum en mode deepsleep')
%% Seccio prova 2: com to gateway -wifi -led
filename = 'P2';
sheet = 1;

dades = xlsread(filename,sheet);
time=dades(:,1);
volt=dades(:,2);

figure(); plot(time,volt);
xlabel('Time(s)')
ylabel('Voltatge(V)')
title('Resposta de la prova amb comunicacio LoRaWAN')
%%
ids_deepsleep=find(volt>4.97)

figure(); plot(time(ids_deepsleep),(5-volt(ids_deepsleep))*1000);
xlabel('Time(s)')
ylabel('Voltatge(mV)')
title('Detall del consum en mode deepsleep')

consum_deep=5-volt(ids_deepsleep);
mean(consum_deep)
std(consum_deep)

figure(); plot(time(ids_deepsleep),(5-volt(ids_deepsleep))*1000,time(ids_deepsleep),mean(consum_deep));
xlabel('Time(s)')
ylabel('Voltatge(mV)')
title('Detall del consum en mode deepsleep')
