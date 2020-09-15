%root='C:\Users\Vicenç Salas\Desktop\CAP1\Entre_Labs';
filename = 'ProvaDinsLab5m';
sheet = 1;

dadesC1 = xlsread(filename,1);
dadesC2 = xlsread(filename,2);
t=dadesC1(:,1);
volt_C1=dadesC1(:,2);
volt_C2=dadesC2(:,2);
figure(); plot(t,volt_C1,t,volt_C2);
xlabel('Time(s)')
ylabel('Voltatge(V)')
title('Consum de la placa en prova 5m')
legend('Consum Lopy','Pin P12')

time=t;
y1=5-volt_C1;
y2=volt_C2;

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
t_sendGTW=t(find(time>15.6-offset_t & time<20.87+offset_t));
y1_sendGTW=y1(find(time>15.6-offset_t & time<20.87+offset_t));
y2_sendGTW=y2(find(time>15.6-offset_t & time<20.87+offset_t));
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
t_sendGTW=t(find(time>14.3-offset_t & time<14.78+offset_t));
y1_sendGTW=y1(find(time>14.3-offset_t & time<14.78+offset_t));
y2_sendGTW=y2(find(time>14.3-offset_t & time<14.78+offset_t));
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
t_sendGTW=t(find(time>11.37-offset_t & time<14.07+offset_t));
y1_sendGTW=y1(find(time>11.37-offset_t & time<14.07+offset_t));
y2_sendGTW=y2(find(time>11.37-offset_t & time<14.07+offset_t));
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
t_sendGTW=t(find(time>10.85-offset_t & time<11.07+offset_t));
y1_sendGTW=y1(find(time>10.85-offset_t & time<11.07+offset_t));
y2_sendGTW=y2(find(time>10.85-offset_t & time<11.07+offset_t));
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
t_mcp=t(find(time>9.5-offset_t & time<10.25+offset_t));
y1_mcp=y1(find(time>9.5-offset_t & time<10.25+offset_t));
y2_mcp=y2(find(time>9.5-offset_t & time<10.25+offset_t));
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
t_bmp=t(find(time>8-offset_t & time<9.2+offset_t));
y1_bmp=y1(find(time>8-offset_t & time<9.2+offset_t));
y2_bmp=y2(find(time>8-offset_t & time<9.2+offset_t));
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
t_start=t(find(time>7.5-offset_t & time<8+offset_t));
y1_start=y1(find(time>7.5-offset_t & time<8+offset_t));
y2_start=y2(find(time>7.5-offset_t & time<8+offset_t));
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