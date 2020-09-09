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
title('Consum de la placa en prova 7m Prova1')
legend('Consum Lopy','Pin P12')

%dadesC1 = xlsread(filename,3);
%dadesC2 = xlsread(filename,4);
%time=dadesC1(:,1);
%volt_C1=dadesC1(:,2);
%volt_C2=dadesC2(:,2);
figure();
subplot(2,1,1);
plot(t,y1)
ylabel('Consum LoPy (A)');
xlabel('Temps (s)')
title('Consums durant la prova 7m')

subplot(2,1,2); 
plot(t,y2);
title('Pin P12');
xlabel('Temps (s)')
ylabel('Tensió a P12 (V)')


offset_t=0.5 %s
%% Localitzar quan envia al GTW
t_sendGTW=t(find(time>1.6-offset_t & time<6.6+offset_t));
y1_sendGTW=y1(find(time>1.6-offset_t & time<6.6+offset_t));
y2_sendGTW=y2(find(time>1.6-offset_t & time<6.6+offset_t));
figure();
subplot(2,1,1);
plot(t_sendGTW,y1_sendGTW);
title('Consums enviant al GTW');
xlabel('Temps (s)')
ylabel('Consum LoPy (A)')

subplot(2,1,2); 
plot(t_sendGTW,y2_sendGTW);
title('Pin P12');
xlabel('Temps (s)')
ylabel('Tensió a P12 (V)')
%% Lectura HTU
t_sendGTW=t(find(time>0.3-offset_t & time<0.79+offset_t));
y1_sendGTW=y1(find(time>0.3-offset_t & time<0.79+offset_t));
y2_sendGTW=y2(find(time>0.3-offset_t & time<0.79+offset_t));
figure();
subplot(2,1,1);
plot(t_sendGTW,y1_sendGTW);
title('Consums llegint sensor HTU');
xlabel('Temps (s)')
ylabel('Consum LoPy (A)')

subplot(2,1,2); 
plot(t_sendGTW,y2_sendGTW);
title('Pin P12');
xlabel('Temps (s)')
ylabel('Tensió a P12 (V)')

%% Lectura camera
t_sendGTW=t(find(time>9.68-offset_t & time<12.54+offset_t));
y1_sendGTW=y1(find(time>9.68-offset_t & time<12.54+offset_t));
y2_sendGTW=y2(find(time>9.68-offset_t & time<12.54+offset_t));
figure();
subplot(2,1,1);
plot(t_sendGTW,y1_sendGTW);
title('Consums llegint sensor camera');
xlabel('Temps (s)')
ylabel('Consum LoPy (A)')

subplot(2,1,2); 
plot(t_sendGTW,y2_sendGTW);
title('Pin P12');
xlabel('Temps (s)')
ylabel('Tensió a P12 (V)')
%% Lectura QAire
t_sendGTW=t(find(time>9.16-offset_t & time<9.367+offset_t));
y1_sendGTW=y1(find(time>9.16-offset_t & time<9.367+offset_t));
y2_sendGTW=y2(find(time>9.16-offset_t & time<9.367+offset_t));
figure();
subplot(2,1,1);
plot(t_sendGTW,y1_sendGTW);
title('Consums llegint sensor qualitat de aire');
xlabel('Temps (s)')
ylabel('Consum LoPy (A)')

subplot(2,1,2); 
plot(t_sendGTW,y2_sendGTW);
title('Pin P12');
xlabel('Temps (s)')
ylabel('Tensió a P12 (V)')

%% Lectura MCP
t_mcp=t(find(time>7.805-offset_t & time<8.52+offset_t));
y1_mcp=y1(find(time>7.805-offset_t & time<8.52+offset_t));
y2_mcp=y2(find(time>7.805-offset_t & time<8.52+offset_t));
figure();
subplot(2,1,1);
plot(t_mcp,y1_mcp);
title('Consums llegint sensor mcp9808');
xlabel('Temps (s)')
ylabel('Consum LoPy (A)')

subplot(2,1,2); 
plot(t_mcp,y2_mcp);
title('Pin P12');
xlabel('Temps (s)')
ylabel('Tensió a P12 (V)')

%% Lectura bmp
t_bmp=t(find(time>6.28-offset_t & time<7.49+offset_t));
y1_bmp=y1(find(time>6.28-offset_t & time<7.49+offset_t));
y2_bmp=y2(find(time>6.28-offset_t & time<7.49+offset_t));
figure();
subplot(2,1,1);
plot(t_bmp,y1_bmp);
title('Consums llegint sensor bmp');
xlabel('Temps (s)')
ylabel('Consum LoPy (A)')

subplot(2,1,2); 
plot(t_bmp,y2_bmp);
title('Pin P12');
xlabel('Temps (s)')
ylabel('Tensió a P12 (V)')
%% Lectura start
t_start=t(find(time>5.76-offset_t & time<6.28+offset_t));
y1_start=y1(find(time>5.76-offset_t & time<6.28+offset_t));
y2_start=y2(find(time>5.76-offset_t & time<6.28+offset_t));
figure();
subplot(2,1,1);
plot(t_start,y1_start);
title('Consums durant el timesleep de start');
xlabel('Temps (s)')
ylabel('Consum LoPy (A)')

subplot(2,1,2); 
plot(t_start,y2_start);
title('Pin P12');
xlabel('Temps (s)')
ylabel('Tensió a P12 (V)')